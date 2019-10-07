import json

import openpyxl
from case_study.models import Tag
from core.decorators import staff_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .common import populate_data, delete_model, patch_model
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


def render_tag_view(request, message=None, message_type=None):
    data = populate_data(schema_tag, Tag.objects.all())
    c = {
        "title": "Tag Admin",
        "model_name": "Tag",
        "toolbar_new": True,
        "toolbar_import": True,
        "data": data,
        "import_form": TagImportForm(),
        "import_endpoint": "/caseadmin/tags/import",
        "schema": schema_tag,
        "admin_message": message,
        "admin_message_type": message_type,
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
        return render_tag_view(request,
                               "Failed to import tags as text/plain. "
                               "Please ensure your text file contains one tag per line. ",
                               "alert-danger")
    tags = []
    for tag in file.file.readlines():
        t = tag.decode("utf-8").strip()
        tags.append(Tag(name=t))
    try:
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        return render_tag_view(request, "Successfully imported {} tags.".format(len(tags)), "alert-success")
    except IntegrityError as e:
        return render_tag_view(request,
                               "Failed to import tags as text/plain. "
                               "Please ensure your text file contains one tag per line. "
                               "Error: " + str(e.args[0]),
                               "alert-danger")


def tag_import_csv(request, file, file_format):
    if file.content_type != "text/csv":
        return render_tag_view(request,
                               "Failed to import tags as text/csv. "
                               "Please ensure your csv file contains one tag per line. ",
                               "alert-danger")
    tags = []
    lines = file.read().decode("utf-8").split("\n")
    for line in lines:
        t = line.strip()
        tags.append(Tag(name=t))
    try:
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        return render_tag_view(request, "Successfully imported {} tags.".format(len(tags)), "alert-success")
    except IntegrityError as e:
        return render_tag_view(request,
                               "Failed to import tags as text/csv. "
                               "Please ensure your csv file contains one tag per line. "
                               "Error: " + str(e.args[0]),
                               "alert-danger")


def tag_import_json(request, file, file_format):
    if file.content_type != "application/json":
        return render_tag_view(request,
                               "Failed to import tags as application/json. "
                               "Please ensure your json file contains a list of strings. ",
                               "alert-danger")
    tags = []
    file_text = file.read().decode("utf-8")
    file_json = json.loads(file_text)
    for tag in file_json:
        t = tag.strip()
        tags.append(Tag(name=t))
    try:
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        return render_tag_view(request, "Successfully imported {} tags.".format(len(tags)), "alert-success")
    except IntegrityError as e:
        return render_tag_view(request,
                               "Failed to import tags as application/json. "
                               "Please ensure your json file contains a list of strings. "
                               "Error: " + str(e.args[0]),
                               "alert-danger")


def tag_import_xlsx(request, file, file_format):
    if not (str(file.content_type) == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or file.name.endswith('.xlsx')):
        return render_tag_view(request,
                               "Failed to import tags as xlsx. "
                               "Please ensure column A has a single tag per cell. ",
                               "alert-danger")
    tags = []
    wb = openpyxl.load_workbook(file)
    sheet = wb.worksheets[0]
    for col in sheet.iter_cols():
        for cel in col:
            t = str(cel.value).strip()
            tags.append(Tag(name=t))

    try:
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        return render_tag_view(request, "Successfully imported {} tags.".format(len(tags)), "alert-success")
    except IntegrityError as e:
        return render_tag_view(request,
                               "Failed to import tags as xlsx. "
                               "Please ensure column A has a single tag per cell. "
                               "Error: " + str(e.args[0]),
                               "alert-danger")


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
            return render_tag_view(request, "Unknown file format: {}".format(str(file_format)), "alert-danger")
    else:
        return JsonResponse({
            "success": False,
            "message": "Unsupported method: " + request.method,
        })


@staff_required
def view_admin_tag(request):
    if request.method == "GET":
        data = populate_data(schema_tag, Tag.objects.all())
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
