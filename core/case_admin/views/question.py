import json

import openpyxl
from case_study.models import Question
from core.decorators import staff_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render

from .common import populate_data, delete_model, patch_model
from ..forms import QuestionImportForm

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


def render_question_view(request, message=None, message_type=None):
    data = populate_data(schema_question, Question)
    c = {
        "title": "Question Admin",
        "model_name": "Question",
        "toolbar_new": True,
        "toolbar_import": True,
        "data": data,
        "import_form": QuestionImportForm(),
        "import_endpoint": "/caseadmin/questions/import",
        "schema": schema_question,
        "admin_message": message,
        "admin_message_type": message_type,

    }
    return render(request, "case-admin.html", c)


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


def question_import_txt(request, file, file_format):
    if file.content_type != "text/plain":
        return render_question_view(request,
                                    "Failed to import questions as text/plain. "
                                    "Please ensure your text file contains one question per line. ",
                                    "alert-danger")
    questions = []
    for question in file.file.readlines():
        q = question.decode("utf-8").strip()
        questions.append(Question(body=q))
    try:
        Question.objects.bulk_create(questions, ignore_conflicts=True)
        return render_question_view(request, "Successfully imported {} questions.".format(len(questions)), "alert-success")
    except IntegrityError as e:
        return render_question_view(request,
                                    "Failed to import questions as text/plain. "
                                    "Please ensure your text file contains one question per line. "
                                    "Error: " + str(e.args[0]),
                                    "alert-danger")


def question_import_csv(request, file, file_format):
    if file.content_type != "text/csv":
        return render_question_view(request,
                                    "Failed to import questions as text/csv. "
                                    "Please ensure your csv file contains one question per line. ",
                                    "alert-danger")
    questions = []
    lines = file.read().decode("utf-8").split("\n")
    for line in lines:
        q = line.strip()
        questions.append(Question(body=q))
    try:
        Question.objects.bulk_create(questions, ignore_conflicts=True)
        return render_question_view(request, "Successfully imported {} questions.".format(len(questions)), "alert-success")
    except IntegrityError as e:
        return render_question_view(request,
                                    "Failed to import questions as text/csv. "
                                    "Please ensure your csv file contains one question per line. "
                                    "Error: " + str(e.args[0]),
                                    "alert-danger")


def question_import_json(request, file, file_format):
    if file.content_type != "application/json":
        return render_question_view(request,
                                    "Failed to import questions as application/json. "
                                    "Please ensure your json file contains a list of strings. ",
                                    "alert-danger")
    questions = []
    file_text = file.read().decode("utf-8")
    file_json = json.loads(file_text)
    for question in file_json:
        q = question.strip()
        questions.append(Question(body=q))
    try:
        Question.objects.bulk_create(questions, ignore_conflicts=True)
        return render_question_view(request, "Successfully imported {} questions.".format(len(questions)), "alert-success")
    except IntegrityError as e:
        return render_question_view(request,
                                    "Failed to import questions as application/json. "
                                    "Please ensure your json file contains a list of strings. "
                                    "Error: " + str(e.args[0]),
                                    "alert-danger")


def question_import_xlsx(request, file, file_format):
    if not (str(file.content_type) == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or file.name.endswith('.xlsx')):
        return render_question_view(request,
                                    "Failed to import questions as xlsx. "
                                    "Please ensure column A has a single question per cell. ",
                                    "alert-danger")
    questions = []
    wb = openpyxl.load_workbook(file)
    sheet = wb.worksheets[0]
    for col in sheet.iter_cols():
        for cel in col:
            q = str(cel.value).strip()
            questions.append(Question(body=q))

    try:
        Question.objects.bulk_create(questions, ignore_conflicts=True)
        return render_question_view(request, "Successfully imported {} questions.".format(len(questions)), "alert-success")
    except IntegrityError as e:
        return render_question_view(request,
                                    "Failed to import questions as xlsx. "
                                    "Please ensure column A has a single question per cell. "
                                    "Error: " + str(e.args[0]),
                                    "alert-danger")


@staff_required
def api_admin_question_import(request):
    if request.method == "POST":
        form = QuestionImportForm(request.POST)
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
            return question_import_csv(request, file, file_format)
        elif file_format == "json":
            return question_import_json(request, file, file_format)
        elif file_format == "xlsx":
            return question_import_xlsx(request, file, file_format)
        elif file_format == "xls":
            return question_import_xlsx(request, file, file_format)
        elif file_format == "txt":
            return question_import_txt(request, file, file_format)
        else:
            return render_question_view(request,
                                        "Unknown file format: {}".format(str(file_format)),
                                        "alert-danger")
    else:
        return JsonResponse({
            "success": False,
            "message": "Unsupported method: " + request.method,
        })


@staff_required
def view_admin_question(request):
    if request.method == "GET":
        return render_question_view(request)
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
