from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sessions.models import Session
from accounts.models import User
from case_study.models import CaseStudy, Tag, Question, TagRelationship, MedicalHistory, Medication
from core.decorators import staff_required
from django.db import IntegrityError
import copy
import json
from .forms import TagImportForm
import openpyxl
from datetime import datetime
import json
from django.db import transaction
from django.core.exceptions import FieldDoesNotExist

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
    "fields": [
        {
            "title": "Date Created",
            "key": "date_created",
            "hide_in_table": True,
            "value_format": "datetime-local",
            "widget": {
                "template": "w-datetime.html",
            },
            "write": True,
        },
        {
            "title": "Date Submitted",
            "key": "date_submitted",
            "hide_in_table": True,
            "value_format": "datetime-local",
            "widget": {
                "template": "w-datetime.html",
            },
            "write": True,
        },
        {
            "title": "Is Submitted",
            "key": "is_submitted",
            "widget": {
                "template": "w-checkbox.html",
            },
            "write": True,
        },
        {
            "title": "Is Anonymous",
            "key": "is_anonymous",
            "hide_in_table": True,
            "widget": {
                "template": "w-checkbox.html",
            },
            "write": True,
        },
        {
            "title": "Author",
            "type": "foreignkey",
            "model": User,
            "allow_null": True,
            "key": "created_by",
            "widget": {
                "template": "w-select.html",
            },
            "write": True,
        },
        {
            "title": "Date Last Edited",
            "key": "date_last_edited",
            "hide_in_table": True,
            "value_format": "datetime-local",
            "widget": {
                "template": "w-datetime.html",
            },
            "write": True,
        },
        {
            "title": "User Last Edited",
            "type": "foreignkey",
            "model": User,
            "allow_null": True,
            "key": "last_edited_user",
            "hide_in_table": True,
            "widget": {
                "template": "w-select.html",
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
            "title": "Height",
            "key": "height",
            "widget": {
                "template": "w-number.html",
            },
            "write": True,
        },
        {
            "title": "Weight",
            "key": "weight",
            "widget": {
                "template": "w-number.html",
                "step": "0.1",
            },
            "write": True,
        },
        {
            "title": "Scr",
            "key": "scr",
            "widget": {
                "template": "w-number.html",
                "step": "0.1",
            },
            "write": True,
        },
        {
            "title": "Age Type",
            "key": "age_type",
            "hide_in_table": True,
            "widget": {
                "template": "w-text.html",
            },
            "write": True,
        },
        {
            "title": "Age (months)",
            "key": "age",
            "widget": {
                "template": "w-number.html",
            },
            "write": True,
        },
        {
            "title": "Sex",
            "key": "sex",
            "widget": {
                "template": "w-text.html",
            },
            "write": True,
        },
        {
            "title": "Description",
            "key": "description",
            "widget": {
                "template": "w-textarea.html",
            },
            "write": True,
        },
        {
            "title": "Medical History",
            "type": "foreignkey-multiple-custom",
            "model": {
                "model": MedicalHistory,
                "key": "body",
                "related_fkey": "case_study",
            },
            "key": "mhx",
            "widget": {
                "template": "w-foreignkey-collection.html",
                "multiple": True,
                "tags": True
            },
            "write": True,
        },
        {
            "title": "Medication",
            "type": "foreignkey-multiple-custom",
            "model": {
                "model": Medication,
                "key": "name",
                "related_fkey": "case_study",
            },
            "key": "medication",
            "widget": {
                "template": "w-foreignkey-collection.html",
                "multiple": True,
                "tags": True
            },
            "write": True,
        },
        {
            "title": "Tags",
            "type": "foreignkey-multiple-relation",
            "model": {
                "model": Tag,
                "key": "name",
            },
            "relation": {
                "model": TagRelationship,
                "model_fkey": "tag",
                "related_fkey": "case_study",
            },
            "key": "tags",
            "widget": {
                "template": "w-foreignkey-collection.html",
                "multiple": True,
            },
            "write": True,
        },
        {
            "title": "Question",
            "type": "foreignkey",
            "model": Question,
            "allow_null": True,
            "key": "question",
            "widget": {
                "template": "w-select.html",
            },
            "write": True,
        },
        {
            "title": "Answer A",
            "key": "answer_a",
            "hide_in_table": True,
            "widget": {
                "template": "w-text.html",
            },
            "write": True,
        },
        {
            "title": "Answer B",
            "key": "answer_b",
            "hide_in_table": True,
            "widget": {
                "template": "w-text.html",
            },
            "write": True,
        },
        {
            "title": "Answer C",
            "key": "answer_c",
            "hide_in_table": True,
            "widget": {
                "template": "w-text.html",
            },
            "write": True,
        },
        {
            "title": "Answer D",
            "key": "answer_d",
            "hide_in_table": True,
            "widget": {
                "template": "w-text.html",
            },
            "write": True,
        },
        {
            "title": "Answer",
            "key": "answer",
            "widget": {
                "template": "w-text.html",
            },
            "write": True,
        },
        {
            "title": "Feedback",
            "key": "feedback",
            "widget": {
                "template": "w-textarea.html",
            },
            "write": True,
        },
    ],
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


value_formatters = {
    "": lambda val: val,
    "datetime-local": lambda val: val.strftime("%Y-%m-%dT%H:%M") if val else val,
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
            key = d.get("key", None)
            d["entity"] = r.id
            d["value"] = vars(r).get(key, None)

            # send empty string instead of python None
            if d["value"] is None:
                d["value"] = ""

            # format the value if required
            if d.get("value_format", None):
                formatter = value_formatters.get(d.get("value_format", ""), None)
                if formatter:
                    d["value"] = formatter(d["value"])

            # handle action fields
            if d.get("type", "") == "action":
                d["value"] = f["widget"]["text"]
            # handle foreign key fields
            elif d.get("type", "") == "foreignkey":
                # get the selected entity
                d["selected"] = vars(r).get(key + "_id", "null")
                # get the foreign key's model
                m = d.get("model", None)
                if m:
                    # add all the possible options to the dropdown and mark the selected one
                    opts = []
                    selected = None
                    for opt in m.objects.all():
                        is_sel = d["selected"] == opt.id
                        opts.append({
                            "id": opt.id,
                            "name": str(opt),
                            "selected": is_sel,
                        })
                        if is_sel:
                            # save value here while we have more data than just ID
                            d["value"] = str(opt)
                    # if this field allows null add a null option to the top of the dropdown
                    if f["allow_null"]:
                        opts.insert(0, {
                            "id": "null",
                            "name": "----------",
                            "selected": d["selected"] == "null"
                        })
                    d["options"] = opts
            # handle foreign key collections with cutom user input (select2.tags = true)
            elif d.get("type", "") == "foreignkey-multiple-custom":
                # the model is the actual data we are interested in linking to our entity
                fk_mod = d.get("model", None)
                # the relation is the model that links us
                if fk_mod:
                    # get all the objects belonging to this entity
                    kwargs = {fk_mod.get("related_fkey", ""): int(r.id)}
                    selected_models = fk_mod["model"].objects.filter(**kwargs)
                    # get all the models these relations point to
                    opts = []
                    for s in selected_models:
                        opts.append({
                            "id": str(s),
                            "name": str(s),
                            "selected": True,
                        })
                    d["options"] = opts
            # handle foreign key collections when they relate two models together with a thrid
            elif d.get("type", "") == "foreignkey-multiple-relation":
                # the model is the actual data we are interested in linking to our entity
                fk_mod = d.get("model", None)
                # the relation is the model that links us
                fk_rel = d.get("relation", None)
                if fk_mod and fk_rel:
                    # get all the relation objects belonging to this entity
                    kwargs = {fk_rel.get("related_fkey", ""): int(r.id)}
                    selected_relations = fk_rel["model"].objects.filter(**kwargs)
                    # get all the models these relations point to
                    selected_models = []
                    for s in selected_relations:
                        selected_models.append(vars(s).get(fk_rel.get("model_fkey", "") + "_id"))
                    # add all the possible options to the dropdown and mark the selected ones
                    opts = []
                    for opt in fk_mod["model"].objects.all():
                        is_selected = False
                        for sel_id in selected_models:
                            if sel_id == opt.id:
                                is_selected = True
                                break
                        opts.append({
                            "id": opt.id,
                            "name": str(opt),
                            "selected": is_selected
                        })
                    d["options"] = opts
            row_data.append(d)
        data["entities"].append(row_data)
    return data


@transaction.atomic
def patch_model(request, model, schema, entity_id):
    # get all the updates the client has requested
    updates = json.loads(request.body)
    # only apply updates to fields that are writable in the schema
    obj = get_object_or_404(model, pk=entity_id)  # get the entity
    for field in schema["fields"]:
        if field.get("type", "") == "foreignkey-multiple-custom":
            key = field["key"]
            fk_model = field.get("model", None)
            selected_fks = updates.get(key, None)
            # delete all current relations
            kwargs = {fk_model["related_fkey"]: entity_id}
            fk_model["model"].objects.filter(**kwargs).delete()
            # create new relations based on the selected fks
            new_models = []
            for sfk in selected_fks:
                entity_model = model.objects.get(id=entity_id)
                kwargs = {
                    fk_model["key"]: str(sfk),
                    fk_model["related_fkey"]: entity_model,
                }
                new_model = fk_model["model"](**kwargs)
                new_models.append(new_model)
            fk_model["model"].objects.bulk_create(new_models)
        elif field.get("type", "") == "foreignkey-multiple-relation":
            key = field["key"]
            fk_model = field.get("model", None)
            fk_relation = field.get("relation", None)
            selected_fks = updates.get(key, None)
            # delete all current relations
            kwargs = {fk_relation["related_fkey"]: entity_id}
            fk_relation["model"].objects.filter(**kwargs).delete()
            # create new relations based on the selected fks
            new_relations = []
            for sfk in selected_fks:
                entity_relation = model.objects.get(id=entity_id)
                entity_model = fk_model["model"].objects.get(id=int(sfk))
                kwargs = {
                    fk_relation["model_fkey"]: entity_model,
                    fk_relation["related_fkey"]: entity_relation,
                }
                new_rel = fk_relation["model"](**kwargs)
                new_relations.append(new_rel)
            fk_relation["model"].objects.bulk_create(new_relations)
        elif field.get("type", "") != "action":  # ignore action fields
            key = field.get("key")
            if key:
                # default to what the entity already had, then to None
                default_val = getattr(obj, key, None)
                try:
                    model_type = model._meta.get_field(key).get_internal_type()
                except FieldDoesNotExist:
                    model_type = None
            else:
                default_val = None
                model_type = None
            new_val = updates.get(key, default_val)
            if model_type == "ForeignKey":
                if new_val == "null":
                    new_val = None
                else:
                    fkm = field.get("model", None)
                    if fkm is not None:
                        if new_val == "":
                            new_val = None
                        else:
                            new_val = fkm.objects.filter(pk=new_val)[0]
            if model_type == "DateTimeField":
                try:
                    new_val = datetime.strptime(new_val, '%Y-%m-%dT%H:%M%S')
                except:
                    new_val = None
            elif model_type == "IntegerField" or model_type == "FloatField" and new_val == "":
                new_val = 0
            try:
                setattr(obj, key, new_val)
            except Exception as e:
                if key:
                    setattr(obj, key, default_val)
                    print("Failed to update field:", key+": Reverting to original value:", e)
    obj.save()
    return JsonResponse({
        "success": True,
    })


@transaction.atomic
def delete_model_soft(request, model, entity_id):
    obj = get_object_or_404(model, pk=entity_id)
    obj.is_deleted = True
    obj.save()
    return JsonResponse({
        "success": True,
    })


@transaction.atomic
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


def case_action_add_tag(request, usr):

    return JsonResponse({
        "success": False,
        "message": "This user does not currently have a log in session.",
    })


def case_action(request, case_id):
    # get all the updates the user has requested
    case = get_object_or_404(CaseStudy, pk=case_id)  # get the user
    data = json.loads(request.body)
    action = data["action"]
    if action == "ADD_TAG":
        return case_action_add_tag(request, case)
    else:
        return JsonResponse({
            "success": False,
            "message": "Unknown action: " + action,
        })


@staff_required
def api_admin_case(request, case_id):
    if request.method == "PATCH":
        return patch_model(request, CaseStudy, schema_case, case_id)
    elif request.method == "DELETE":
        return delete_model_soft(request, CaseStudy, case_id)
    elif False and request.method == "PUT":  # use PUT for actions
        return case_action(request, case_id)
    else:
        return JsonResponse({
            "success": False,
            "message": "Unsupported HTTP method: " + request.method
        })


@staff_required
def view_admin_case(request):
    data = populate_data(schema_case, CaseStudy)
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
    if file.content_type != "text/plain":
        return JsonResponse({
            "success": False,
            "message": "Failed to import tags as text/plain\n\n"
                       "Please ensure your text file contains one tag per line",
        })
    tags = []
    for tag in file.file.readlines():
        t = tag.decode("utf-8").strip()
        tags.append(Tag(name=t))
    try:
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        return JsonResponse({
            "success": True,
            "message": "Imported {} tags".format(len(tags)),
        })
    except IntegrityError as e:
        return JsonResponse({
            "success": False,
            "message": "Failed to import tags as text/plain\n\n"
                       "Please ensure your text file contains one tag per line\n\n"
                       "Error: " + str(e.args[0]),
        })


def tag_import_csv(request, file, file_format):
    if file.content_type != "text/csv":
        return JsonResponse({
            "success": False,
            "message": "Failed to import tags as text/csv\n\n"
                       "Please ensure your csv file contains one tag per line",
        })
    tags = []
    lines = file.read().decode("utf-8").split("\n")
    for line in lines:
        t = line.strip()
        tags.append(Tag(name=t))
    try:
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        return JsonResponse({
            "success": True,
            "message": "Imported {} tags".format(len(tags)),
        })
    except IntegrityError as e:
        return JsonResponse({
            "success": False,
            "message": """Failed to import tags as text/csv

            Please ensure your csv file contains one tag per line

            Error: """ + str(e.args[0]),
        })


def tag_import_json(request, file, file_format):
    if file.content_type != "application/json":
        return JsonResponse({
            "success": False,
            "message": "Failed to import tags as application/json\n\n"
                       "Please ensure your json file contains a list of strings",
        })
    tags = []
    file_text = file.read().decode("utf-8")
    file_json = json.loads(file_text)
    for tag in file_json:
        t = tag.strip()
        tags.append(Tag(name=t))
    try:
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        return JsonResponse({
            "success": True,
            "message": "Imported {} tags".format(len(tags)),
        })
    except IntegrityError as e:
        return JsonResponse({
            "success": False,
            "message": "Failed to import tags as application/json\n\n"
                       "Please ensure your json file contains a list of strings\n\n"
                       "Error: " + str(e.args[0]),
        })


def tag_import_xlsx(request, file, file_format):
    if not (str(file.content_type) == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or file.name.endswith('.xlsx')):
        return JsonResponse({
            "success": False,
            "message": "Failed to import tags as xlsx\n\n"
                       "Please ensure column A has a single tag per cell\n\n",
        })
    tags = []
    wb = openpyxl.load_workbook(file)
    sheet = wb.worksheets[0]
    for col in sheet.iter_cols():
        for cel in col:
            t = str(cel.value).strip()
            tags.append(Tag(name=t))

    try:
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        return JsonResponse({
            "success": True,
            "message": "Imported {} tags".format(len(tags)),
        })
    except IntegrityError as e:
        return JsonResponse({
            "success": False,
            "message": "Failed to import tags as xlsx\n\n"
                       "Please ensure column A has a single tag per cell\n\n"
                       "Error: " + str(e.args[0]),
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
            elif file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or file.name.endswith('.xlsx'):
                file_format = "xlsx"
            elif file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or file.name.endswith('.xls'):
                file_format = "xls"
            elif file.content_type == "text/plain":
                file_format = "txt"

        if file_format == "csv":
            return tag_import_csv(request, file, file_format)
        elif file_format == "json":
            return tag_import_json(request, file, file_format)
        elif file_format == "xlsx":
            return tag_import_xlsx(request, file, file_format)
        elif file_format == "xls":
            return tag_import_xlsx(request, file, file_format)
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
