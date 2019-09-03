from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sessions.models import Session
from accounts.models import User
from case_study.models import CaseStudy, Tag
from core.decorators import staff_required
from django.db import IntegrityError
import copy
import json
import csv
import base64
from .forms import TagImportForm


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
    "fields": [
        {
            "title": "Tag",
            "key": "name",
            "widget": {
                "template": "w-text.html",
                "maxlength": 60,
            },
            "write": True,
        },
    ]
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


def patch_model(request, model, schema, entity_id):
    # get all the updates the client has requested
    updates = json.loads(request.body)
    # only apply updates to fields that are writable in the schema
    obj = get_object_or_404(model, pk=entity_id)  # get the entity
    for field in schema["fields"]:
        if field.get("type", "") != "action":  # ignore action fields
            key = field["key"]
            default_val = getattr(obj, key, None)  # default to what the entity already had, then to None
            new_val = updates.get(key, default_val)
            setattr(obj, key, new_val)
    obj.save()  # save the user to the db
    return JsonResponse({
        "success": True,
    })


def delete_model_soft(request, model, entity_id):
    obj = get_object_or_404(model, pk=entity_id)
    obj.is_deleted = True
    obj.save()
    return JsonResponse({
        "success": True,
    })


def delete_model(request, model, entity_id):
    model.objects.filter(id=entity_id).delete()
    return JsonResponse({
        "success": True,
    })


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
    if action == "RESET_PASSWORD":
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
        return delete_model_soft(request, user_id)
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
    data = populate_data(schema_user, User)
    c = {
        "title": "User Admin",
        "model_name": "User",
        "data": data,
        "schema": schema_user,
    }
    return render(request, "case-admin.html", c)


@staff_required
def view_admin_case(request):
    data = populate_data(schema_case, User)
    c = {
        "title": "Case Study Admin",
        "model_name": "Case Study",
        "data": data,
        "schema": schema_case,
    }
    return render(request, "case-admin.html", c)


@staff_required
def view_admin_comment(request):
    data = populate_data(schema_comment, User)
    c = {
        "title": "Comment Admin",
        "model_name": "Comment",
        "data": data,
        "schema": schema_comment,
    }
    return render(request, "case-admin.html", c)


@staff_required
def api_admin_tag(request, tag_id):
    if request.method == "PATCH":
        return patch_model(request, Tag, schema_tag, tag_id)
    elif request.method == "DELETE":
        return delete_model(request, Tag, tag_id)
    else:
        return JsonResponse({
            "success": False,
            "message": "Unsupported HTTP method: " + request.method,
        })


def tag_import_txt(request, file, file_format):
    tags = []
    for tag in file.file.readlines():
        t = tag.decode().strip()
        tags.append(Tag(name=t))
    Tag.objects.bulk_create(tags)
    return JsonResponse({
        "success": True,
        "message": "Imported {} tags".format(len(tags)),
    })


@staff_required
def api_admin_tag_import(request):
    if request.method == "POST":
        form = TagImportForm(request.POST)
        file = request.FILES["file"]
        file_format = str(form["file_format"].value())
        if file_format == "auto":
            if file.content_type == "text/csv":
                file_format = "csv"
            elif file.content_type == "application/json":
                file_format = "json"
            elif file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or \
                    file.name.endswith('.xlsx'):
                file_format = "xlsx"
            elif file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or \
                    file.name.endswith('.xls'):
                file_format = "xls"
            elif file.content_type == "text/plain":
                file_format = "txt"

        if file_format == "csv":
            return JsonResponse({
                "success": False,
                "message": "File typ .csv is NYI",
            })
        elif file_format == "json":
            return JsonResponse({
                "success": False,
                "message": "File typ .json is NYI",
            })
        elif file_format == "xlsx":
            return JsonResponse({
                "success": False,
                "message": "File typ .xlsx is NYI",
            })
        elif file_format == "xls":
            return JsonResponse({
                "success": False,
                "message": "File typ .xls is NYI",
            })
        elif file_format == "txt":
            return tag_import_txt(request, file, file_format)
        else:
            return JsonResponse({
                "success": False,
                "message": "Unknown file format: " + str(file_format),
            })
    else:
        return JsonResponse({
            "success": False,
            "message": "Unsupported method: " + request.method,
        })


@staff_required
def view_admin_tag(request):
    if request.method == "GET":
        data = populate_data(schema_tag, Tag)
        c = {
            "title": "Tag Admin",
            "model_name": "Tag",
            "toolbar_new": True,
            "toolbar_import": True,
            "data": data,
            "import_form": TagImportForm(),
            "import_endpoint": "/caseadmin/tags/import",
            "schema": schema_tag,
        }
        return render(request, "case-admin.html", c)
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            Tag.objects.create(name=body["name"])
            return JsonResponse({
                "success": True,
                "message": "Tag created",
            })
        except IntegrityError as e:
            return JsonResponse({
                "success": False,
                "message": "Failed to create a tag: Tag name must be unique\n" + str(e.args[0]),
            })


@staff_required
def view_default(request):
    return render(request, "case-admin-landing.html")
