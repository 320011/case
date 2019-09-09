import copy
import json
from datetime import datetime

import openpyxl
from accounts.models import User
from case_study.models import CaseStudy, Tag, Question, TagRelationship, MedicalHistory, Medication
from core.decorators import staff_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sessions.models import Session
from django.core.exceptions import FieldDoesNotExist
from django.db import IntegrityError
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from ..forms import TagImportForm

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
