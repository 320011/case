from accounts.models import User
from case_study.models import CaseStudy, Tag, Question, TagRelationship, MedicalHistory, Medication, Other
from core.decorators import staff_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import json

from .common import populate_data, delete_model, patch_model

schema_case = {
    "endpoint": "/caseadmin/cases/",
    "fields": [
        {
            "title": "ID",
            "key": "id",
            "widget": {
                "template": "w-number.html",
            },
            "write": False,
        },
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
            "title": "State",
            "type": "choices",
            "key": "case_state",
            "widget": {
                "template": "w-select.html",
            },
            "choices": [
                ("D", "Draft"),
                ("R", "Review"),
                ("P", "Public")
            ],
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
            "title": "Is Deleted",
            "key": "is_deleted",
            "widget": {
                "template": "w-checkbox.html",
            },
            "write": True,
        },
        {
            "title": "Height (cm)",
            "key": "height",
            "widget": {
                "template": "w-number.html",
            },
            "write": True,
        },
        {
            "title": "Weight (kg)",
            "key": "weight",
            "widget": {
                "template": "w-number.html",
                "step": "0.1",
            },
            "write": True,
        },
        {
            "title": "Scr (μmol/L)",
            "key": "scr",
            "widget": {
                "template": "w-number.html",
                "step": "0.1",
            },
            "write": True,
        },
        {
            "title": "Age Display Type",
            "type": "choices",
            "key": "age_type",
            "hide_in_table": True,
            "widget": {
                "template": "w-select.html",
            },
            "choices": [
                ("Y", "Years"),
                ("M", "Months")
            ],
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
            "type": "choices",
            "key": "sex",
            "widget": {
                "template": "w-select.html",
            },
            "choices": [
                ("M", "Male"),
                ("F", "Female")
            ],
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
            "title": "Other",
            "type": "foreignkey-multiple-custom",
            "model": {
                "model": Other,
                "key": "other_body",
                "related_fkey": "case_study",
            },
            "key": "other",
            "widget": {
                "template": "w-foreignkey-collection.html",
                "multiple": True,
                "tags": True
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
            "title": "Correct Answer",
            "key": "answer",
            "type": "choices",
            "allow_null": False,
            "widget": {
                "template": "w-select.html",
            },
            "write": True,
            "choices": [
                ("A", "A"),
                ("B", "B"),
                ("C", "C"),
                ("D", "D"),
            ],
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


def case_action(request, case_id):
    body = json.loads(request.body)
    action = body["action"]
    if action == "APPROVE":
        CaseStudy.objects.filter(pk=case_id).update(case_state=CaseStudy.STATE_PUBLIC)
        return JsonResponse({
            "success": True,
            "message": "Approved case study"
        })
    elif action == "DENY":
        CaseStudy.objects.filter(id=case_id).delete()
        return JsonResponse({
            "success": True,
            "message": "Denied case study"
        })
    else:
        return JsonResponse({
            "success": False,
            "message": "Unknown action: {}".format(request.body["action"])
        })



@staff_required
def api_admin_case(request, case_id):
    if request.method == "PATCH":
        return patch_model(request, CaseStudy, schema_case, case_id)
    elif request.method == "DELETE":
        return delete_model(request, CaseStudy, case_id)
    elif request.method == "PUT":
        return case_action(request, case_id)
    else:
        return JsonResponse({
            "success": False,
            "message": "Unsupported HTTP method: " + request.method
        })


@staff_required
def view_admin_case(request):
    data = populate_data(schema_case, CaseStudy.objects.all())
    new_case_count = CaseStudy.objects.filter(case_state=CaseStudy.STATE_REVIEW).count()
    c = {
        "title": "Case Study Admin",
        "model_name": "Case Study",
        "data": data,
        "schema": schema_case,
        "toolbar_review": True,
        "review_count": new_case_count,
        "review_endpoint": reverse("case_admin:cases_review"),
    }
    return render(request, "case-admin.html", c)


@staff_required
def view_admin_case_review(request):
    data = populate_data(schema_case, CaseStudy.objects.filter(case_state=CaseStudy.STATE_REVIEW))
    c = {
        "title": "Review Case Studies",
        "model_name": "Case Study",
        "data": data,
        "schema": schema_case,
        "reviewing": True,
        "review_header": "Case Study Review",
        "review_description": "Inspect, modify, and approve case studies that have been submitted for review by users "
                              "of UWA Pharmacy Case.",
        "back_url": reverse("case_admin:cases"),
    }
    return render(request, "case-admin.html", c)
