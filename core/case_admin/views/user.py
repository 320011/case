import json

from accounts.models import User
from core.decorators import staff_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sessions.models import Session
from django.db import IntegrityError
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from accounts.views import send_email_async
from django.contrib.sites.shortcuts import get_current_site

from ..forms import TagImportForm
from .common import populate_data, delete_model, patch_model

schema_user = {
    "endpoint": "/caseadmin/users/",
    "fields": [
        {
            "title": "First Name",
            "key": "first_name",
            "widget": {
                "template": "w-text.html",
                "maxlength": 40,
            },
            "write": True,
        },
        {
            "title": "Last Name",
            "key": "last_name",
            "widget": {
                "template": "w-text.html",
                "maxlength": 60,
            },
            "write": True,
        },
        {
            "title": "Email",
            "key": "email",
            "widget": {
                "template": "w-email.html",
                "maxlength": 250,
            },
            "write": True,
        },
        {
            "title": "University",
            "key": "university",
            "widget": {
                "template": "w-text.html",
                "maxlength": 150,
            },
            "write": True,
        },
        {
            "title": "Degree Start",
            "key": "degree_commencement_year",
            "widget": {
                "template": "w-number.html",
            },
            "write": True,
        },
        {
            "title": "Is Staff",
            "key": "is_staff",
            "widget": {
                "template": "w-checkbox.html",
            },
            "write": True,
        },
        {
            "title": "Is Tutor",
            "key": "is_tutor",
            "widget": {
                "template": "w-checkbox.html",
            },
            "write": True,
        },
        {
            "title": "Is Deleted",
            "key": "is_deleted",
            "widget": {
                "template": "w-checkbox.html",
            },
            "write": True,
        },
        {
            "title": "Password",
            "type": "action",
            "key": "ACTION_RESET_PASSWORD",
            "widget": {
                "template": "w-button.html",
                "text": "Send reset email",
                "action": "RESET_PASSWORD",
            },
            "write": True,
        },
        {
            "title": "Login Session",
            "type": "action",
            "key": "ACTION_LOGOUT",
            "widget": {
                "template": "w-button.html",
                "text": "Log user out",
                "action": "LOGOUT",
            },
            "write": True,
        },
    ]
}

schema_user_review = {
    "endpoint": "/caseadmin/users/",
    "fields": [
        {
            "title": "First Name",
            "key": "first_name",
            "widget": {
                "template": "w-text.html",
                "maxlength": 40,
            },
            "write": True,
        },
        {
            "title": "Last Name",
            "key": "last_name",
            "widget": {
                "template": "w-text.html",
                "maxlength": 60,
            },
            "write": True,
        },
        {
            "title": "Email",
            "key": "email",
            "widget": {
                "template": "w-email.html",
                "maxlength": 250,
            },
            "write": True,
        },
        {
            "title": "University",
            "key": "university",
            "widget": {
                "template": "w-text.html",
                "maxlength": 150,
            },
            "write": True,
        },
        {
            "title": "Degree Start",
            "key": "degree_commencement_year",
            "widget": {
                "template": "w-number.html",
            },
            "write": True,
        },
        {
            "title": "Approve",
            "type": "action",
            "key": "ACTION_APPROVE",
            "widget": {
                "template": "w-button.html",
                "text": "Approve User",
                "action": "APPROVE",
                "reload": True,
            },
            "write": True,
        },
    ]
}


def user_action_reset_password(request, usr):
    form = PasswordResetForm({'email': usr.email})
    if form.is_valid():
        form.save(request=request, from_email=usr.email,
                  email_template_name='registration/password_reset_email.html')
        return JsonResponse({
            "success": True,
            "message": "A password reset link has been sent to the user.",
        })
    else:
        return JsonResponse({
            "success": False,
            "message": "Failed to reset the users password. Bad form.",
        })


def user_action_logout(request, usr):
    found_session = False
    for s in Session.objects.all():
        if int(s.get_decoded().get('_auth_user_id')) == usr.id:
            found_session = True
            s.delete()
            # we could lock the user out here too
            # but we will need a way to reactivate their account later
            # lock out should be its own action
            # usr.is_active = False
            # usr.save()
            return JsonResponse({
                "success": True,
                "message": "The users login session was ended.",
            })
    if found_session:
        return JsonResponse({
            "success": False,
            "message": "Session found but failed to end.",
        })
    else:
        return JsonResponse({
            "success": False,
            "message": "This user does not currently have a log in session.",
        })


def user_action(request, user_id):
    # get all the updates the user has requested
    usr = get_object_or_404(User, pk=user_id)  # get the user
    data = json.loads(request.body)
    action = data["action"]
    if action == "APPROVE":
        User.objects.filter(pk=user_id).update(is_active=True)
        send_email_async("Account Activated",
                         "html",
                         "mail/activate-account.html", {
                             "user": usr,
                             "success": True,
                             "domain": get_current_site(request).domain,
                             "protocol": request.is_secure() and "https" or "http"
                         },
                         from_email='UWA Pharmacy Case',
                         to=[usr.email])
        return JsonResponse({
            "success": True,
            "message": "Approved user"
        })
    elif action == "DENY":
        User.objects.filter(pk=user_id).delete()
        return JsonResponse({
            "success": True,
            "message": "Denied user"
        })
    elif action == "RESET_PASSWORD":
        return user_action_reset_password(request, usr)
    elif action == "LOGOUT":
        return user_action_logout(request, usr)
    else:
        return JsonResponse({
            "success": False,
            "message": "Unknown action: " + action,
        })


@staff_required
def api_admin_user(request, user_id):
    if request.method == "PATCH":
        return patch_model(request, User, schema_user, user_id)
    elif request.method == "DELETE":
        return delete_model(request, User, user_id)
    elif request.method == "PUT":  # use PUT for actions
        return user_action(request, user_id)
    else:
        return JsonResponse({
            "success": False,
            "message": "Unsupported HTTP method: " + request.method
        })


@staff_required
def view_admin_user(request):
    # get returns a template with all the users in a table
    data = populate_data(schema_user, User.objects.all())
    new_user_count = User.objects.filter(is_active=False).count()
    c = {
        "title": "User Admin",
        "model_name": "User",
        "data": data,
        "schema": schema_user,
        "toolbar_review": True,
        "review_count": new_user_count,
        "review_endpoint": reverse("case_admin:users_review"),
    }
    return render(request, "case-admin.html", c)


@staff_required
def view_admin_user_review(request):
    # get returns a template with all the users in a table
    data = populate_data(schema_user_review, User.objects.filter(is_active=False))
    c = {
        "title": "User Admin",
        "model_name": "User",
        "data": data,
        "schema": schema_user_review,
        "reviewing": True,
        "review_header": "User Review",
        "review_description": "Approve users who have recently signed up for the site.",
        "back_url": reverse("case_admin:users"),

    }
    return render(request, "case-admin.html", c)
