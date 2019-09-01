from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sessions.models import Session
from accounts.models import User
from case_study.models import CaseStudy
from core.decorators import staff_required
import copy
import json

schema_user = {
    "endpoint": "/caseadmin/users/",
    "fields": [
        {
            "title": "First Name",
            "key": "first_name",
            "widget": {
                "template": "w-text.html",
                "maxchars": 40,
            },
            "write": True,
        },
        {
            "title": "Last Name",
            "key": "last_name",
            "widget": {
                "template": "w-text.html",
                "maxchars": 60,
            },
            "write": True,
        },
        {
            "title": "Email",
            "key": "email",
            "widget": {
                "template": "w-email.html",
                "maxchars": 250,
            },
            "write": True,
        },
        {
            "title": "University",
            "key": "university",
            "widget": {
                "template": "w-text.html",
                "maxchars": 150,
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
            "widget": {
                "template": "w-button.html",
                "text": "Send Reset Link",
                "action": "RESET_PASSWORD",
            },
            "write": True,
        },
        {
            "title": "Login Session",
            "type": "action",
            "widget": {
                "template": "w-button.html",
                "text": "Log user out",
                "action": "LOGOUT",
            },
            "write": True,
        },
    ]
}

schema_case = {
    "endpoint": "/caseadmin/cases/",
    "fields": [],
}

schema_comment = {
    "endpoint": "/caseadmin/comments/",
    "fields": [],
}

schema_tag = {
    "endpoint": "/caseadmin/tags/",
    "fields": [],
}


def populate_data(schema, model):
    records = model.objects.all()
    data = {
        "endpoint": schema["endpoint"],
        "entities": [],
    }
    # for all records in the db
    for r in records:
        row_data = []  # this rows data
        # add each field to the data
        for f in schema["fields"]:
            d = copy.deepcopy(f)
            if d.get("type", "") != "action":  # actions dont have keys
                d["value"] = vars(r)[d["key"]]
            else:
                d["value"] = f["widget"]["text"]
            d["entity"] = r.id
            row_data.append(d)
        data["entities"].append(row_data)
    return data


def user_ACTION_RESET_PASSWORD(request, usr):
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


def user_ACTION_LOGOUT(request, usr):
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


def user_ACTION(request, user_id):
    # get all the updates the user has requested
    usr = get_object_or_404(User, pk=user_id)  # get the user
    data = json.loads(request.body)
    action = data["action"]
    if action == "RESET_PASSWORD":
        return user_ACTION_RESET_PASSWORD(request, usr)
    elif action == "LOGOUT":
        return user_ACTION_LOGOUT(request, usr)
    else:
        return JsonResponse({
            "success": False,
            "message": "Unknown action: " + action,
        })


def user_PATCH(request, user_id):
    # get all the updates the user has requested
    updates = json.loads(request.body)
    # only apply updates to fields that are writable in the schema
    usr = get_object_or_404(User, pk=user_id)  # get the user
    for field in schema_user["fields"]:
        if field.get("type", "") != "action":  # ignore action fields
            key = field["key"]
            default_val = getattr(usr, key, None)  # default to what the user already had, then to None
            new_val = updates.get(key, default_val)
            setattr(usr, key, new_val)
    usr.save()  # save the user to the db
    return JsonResponse({
        "success": True,
    })


def user_DELETE(request, user_id):
    usr = get_object_or_404(User, pk=user_id)
    usr.is_deleted = True
    usr.save()
    return JsonResponse({
        "success": True,
    })


@staff_required
def api_admin_user(request, user_id):
    if request.method == "PATCH":
        return user_PATCH(request, user_id)
    elif request.method == "DELETE":
        return user_DELETE(request, user_id)
    elif request.method == "POST":  # use POST for actions
        return user_ACTION(request, user_id)
    else:
        return JsonResponse({
            "success": False,
            "message": "Unsupported HTTP method: " + request.method
        })


@staff_required
def view_admin_user(request):
    # get returns a template with all the users in a table
    data = populate_data(schema_user, User)
    c = {
        "title": "User Admin",
        "model_name": "User",
        "data": data,
    }
    return render(request, "case-admin.html", c)


@staff_required
def view_admin_case(request):
    data = populate_data(schema_case, User)
    c = {
        "title": "Case Study Admin",
        "model_name": "Case Study",
        "data": data
    }
    return render(request, "case-admin.html", c)


@staff_required
def view_admin_comment(request):
    data = populate_data(schema_comment, User)
    c = {
        "title": "Comment Admin",
        "model_name": "Comment",
        "data": data
    }
    return render(request, "case-admin.html", c)


@staff_required
def view_admin_tag(request):
    data = populate_data(schema_tag, User)
    c = {
        "title": "Tag Admin",
        "model_name": "Tag",
        "data": data
    }
    return render(request, "case-admin.html", c)


@staff_required
def view_default(request):
    return render(request, "case-admin-landing.html")
