from case_study.models import Comment, CaseStudy
from accounts.models import User
from core.decorators import staff_required
from django.shortcuts import render
from .common import populate_data, delete_model, patch_model
from django.http import JsonResponse

schema_comment = {
    "endpoint": "/caseadmin/comments/",
    "fields": [
        {
            "title": "Date",
            "key": "comment_date",
            "value_format": "datetime-local",
            "widget": {
                "template": "w-datetime.html",
            },
            "write": True,
        },
        {
            "title": "Author",
            "type": "foreignkey",
            "model": User,
            "allow_null": False,
            "key": "user",
            "widget": {
                "template": "w-select.html",
            },
            "write": True,
        },
        {
            "title": "Case Study",
            "type": "foreignkey",
            "model": CaseStudy,
            "allow_null": False,
            "key": "case_study",
            "widget": {
                "template": "w-select.html",
            },
            "write": True,
        },
        {
            "title": "Anonymous",
            "key": "is_anon",
            "widget": {
                "template": "w-checkbox.html",
            },
            "write": True,
        },
        {
            "title": "Body",
            "key": "comment",
            "widget": {
                "template": "w-textarea.html",
            },
            "write": True,
        },
    ],
}


@staff_required
def api_admin_comment(request, comment_id):
    if request.method == "PATCH":
        return patch_model(request, Comment, schema_comment, comment_id)
    elif request.method == "DELETE":
        return delete_model(request, comment_id)
    else:
        return JsonResponse({
            "success": False,
            "message": "Unsupported HTTP method: " + request.method
        })


@staff_required
def view_admin_comment(request):
    if request.method == "GET":
        data = populate_data(schema_comment, Comment.objects.all())
        c = {
            "title": "Comment Admin",
            "model_name": "Comment",
            "data": data,
            "schema": schema_comment,
        }
        return render(request, "case-admin.html", c)


@staff_required
def view_admin_comment_review(request):
    if request.method == "GET":
        data = populate_data(schema_comment, Comment.objects.all())
        c = {
            "title": "Comment Admin",
            "model_name": "Comment",
            "data": data,
            "schema": schema_comment,
        }
        return render(request, "case-admin.html", c)

