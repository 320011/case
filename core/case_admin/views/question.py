import json

import openpyxl
from case_study.models import Question
from core.decorators import staff_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render

from .common import populate_data, delete_model, patch_model
from ..forms import TagImportForm

schema_question = {
    "endpoint": "/caseadmin/questions/",
    "fields": [
        {
            "title": "Question",
            "key": "body",
            "widget": {
                "template": "w-text.html",
            },
            "write": True,
        },
    ]
}


@staff_required
def api_admin_question(request, question_id):
    if request.method == "PATCH":
        return patch_model(request, Question, schema_question, question_id)
    elif request.method == "DELETE":
        return delete_model(request, Question, question_id)
    else:
        return JsonResponse({
            "success": False,
            "message": "Unsupported HTTP method: " + request.method,
        })


@staff_required
def view_admin_question(request):
    if request.method == "GET":
        data = populate_data(schema_question, Question)
        c = {
            "title": "Question Admin",
            "model_name": "Question",
            "toolbar_new": True,
            "data": data,
            "schema": schema_question,
        }
        return render(request, "case-admin.html", c)
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            Question.objects.create(body=body["body"])
            return JsonResponse({
                "success": True,
                "message": "Question created",
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": "Failed to create a question:\n" + str(e.args[0]),
            })
