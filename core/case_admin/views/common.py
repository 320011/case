import copy
import json
from datetime import datetime

from core.decorators import staff_required
from django.core.exceptions import FieldDoesNotExist
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from case_study.models import CaseStudy
from accounts.models import User

value_formatters = {
    "": lambda val: val,
    "datetime-local": lambda val: val.strftime("%Y-%m-%dT%H:%M") if val else val,
}


def populate_data(schema, queryset):
    data = {
        "endpoint": schema["endpoint"],
        "entities": [],
    }
    # for all records in the db
    for r in queryset:
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
            # handle choices fields
            elif d.get("type", "") == "choices":
                opts = []
                for c in d["choices"]:
                    opts.append({
                        "id": c[0],
                        "name": str(c[1]),
                        "selected": c[0] == d["value"],
                    })
                d["options"] = opts
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
            elif (model_type == "IntegerField" or model_type == "FloatField") and new_val == "":
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
def delete_model(request, model, entity_id):
    b = json.loads(request.body)
    if b["hard"]:
        model.objects.filter(id=entity_id).delete()
        return JsonResponse({
            "success": True,
        })
    else:
        obj = get_object_or_404(model, pk=entity_id)
        obj.is_deleted = True
        obj.save()
        return JsonResponse({
            "success": True,
        })


def get_badge_counts():
    total = 0
    new_user_count = User.objects.filter(is_active=False).count()
    total += new_user_count
    new_case_count = CaseStudy.objects.filter(is_submitted=False).count()
    total += new_case_count
    new_comment_report_count = 0#CommentReport.objects.filter(viewed=False).count()
    total += new_comment_report_count
    return {
        "total": total,
        "users": new_user_count,  # number of new users waiting for approval
        "cases": new_case_count,  # number of new cases waiting for approval
        "questions": 0,  # always 0 for now
        "comments": new_comment_report_count,  # number of comment reports waiting for review
        "tags": 0,  # always 0 for now,
    }


@staff_required
def view_landing(request):
    c = {
        "badge_count": get_badge_counts()
    }
    return render(request, "case-admin-landing.html", c)
