from case_study.models import Comment, CaseStudy, CommentReport
from accounts.models import User
from core.decorators import staff_required
from django.db import transaction
from django.shortcuts import render
from .common import populate_data, delete_model, patch_model
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
import json

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
            "title": "Is Anonymous",
            "key": "is_anon",
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
            "title": "Body",
            "key": "comment",
            "widget": {
                "template": "w-textarea.html",
            },
            "write": True,
        },
    ],
}

schema_comment_report = {
    "endpoint": "/caseadmin/comments/",
    "fields": [
        {
            "title": "Comment Date",
            "key": "comment_date",
            "value_format": "datetime-local",
            "widget": {
                "template": "w-datetime.html",
            },
            "write": False,
        },
        {
            "title": "Report Date",
            "key": "report_date",
            "value_format": "datetime-local",
            "widget": {
                "template": "w-datetime.html",
            },
            "write": False,
        },
        {
            "title": "Comment Author",
            "type": "foreignkey",
            "model": User,
            "allow_null": False,
            "key": "comment_author",
            "widget": {
                "template": "w-select.html",
            },
            "write": False,
        },
        {
            "title": "Report Author",
            "type": "foreignkey",
            "model": User,
            "allow_null": False,
            "key": "report_author",
            "widget": {
                "template": "w-select.html",
            },
            "write": False,
        },
        {
            "title": "Comment Body",
            "key": "comment_body",
            "widget": {
                "template": "w-textarea.html",
            },
            "write": False,
        },
        {
            "title": "Report Reason",
            "key": "reason",
            "widget": {
                "template": "w-textarea.html",
            },
            "write": False,
        },
    ],
}


@transaction.atomic
def comment_action(request, comment_id):
    # get all the updates the user has requested
    data = json.loads(request.body)
    action = data["action"]
    # comment_id is actually comment_report_id for these actions
    if action == "SILENCE_REPORT_AUTHOR":
        cr = get_object_or_404(CommentReport, id=comment_id)
        usr = get_object_or_404(User, id=cr.report_author.id)
        usr.is_report_silenced = True
        usr.save()
        cr.report_reviewed = True
        cr.save()
        return JsonResponse({
            "success": True,
            "message": "Report author silenced"
        })
    elif action == "BAN_COMMENT_AUTHOR":
        cr = get_object_or_404(CommentReport, id=comment_id)
        usr = get_object_or_404(User, id=cr.comment_author.id)
        usr.ban()  # this will set is_banned to true and log the user out
        comm = Comment.objects.get(pk=cr.comment.id)  # comments might be deleted as we DO_NOTHING
        if comm:
            comm.is_deleted = True
            comm.save()
        cr.report_reviewed = True
        cr.save()
        return JsonResponse({
            "success": True,
            "message": "User banned and comment deleted"
        })
    elif action == "DELETE_COMMENT":
        cr = get_object_or_404(CommentReport, id=comment_id)
        comm = Comment.objects.get(pk=cr.comment.id)  # comments might be deleted as we DO_NOTHING
        if comm:
            comm.is_deleted = True
            comm.save()
        cr.report_reviewed = True
        cr.save()
        return JsonResponse({
            "success": True,
            "message": "Comment deleted"
        })
    elif action == "DISMISS_REPORT":
        cr = get_object_or_404(CommentReport, id=comment_id)
        cr.report_reviewed = True
        cr.save()
        return JsonResponse({
            "success": True,
            "message": "Report dismissed"
        })


@staff_required
def api_admin_comment(request, comment_id):
    if request.method == "PATCH":
        return patch_model(request, Comment, schema_comment, comment_id)
    elif request.method == "DELETE":
        return delete_model(request, comment_id)
    elif request.method == "PUT":  # use PUT for actions
        return comment_action(request, comment_id)
    else:
        return JsonResponse({
            "success": False,
            "message": "Unsupported HTTP method: " + request.method
        })


@staff_required
def view_admin_comment(request):
    if request.method == "GET":
        data = populate_data(schema_comment, Comment.objects.all())
        comment_report_count = CommentReport.objects.filter(report_reviewed=False, report_author__is_report_silenced=False).count()
        c = {
            "title": "Comment Admin",
            "model_name": "Comment",
            "data": data,
            "schema": schema_comment,
            "toolbar_review": True,
            "review_count": comment_report_count,
            "review_endpoint": reverse("case_admin:comments_review"),
            "review_button_text": "Reports"
        }
        return render(request, "case-admin.html", c)


@staff_required
def view_admin_comment_review(request):
    if request.method == "GET":
        data = populate_data(schema_comment_report, CommentReport.objects.filter(report_reviewed=False, report_author__is_report_silenced=False))
        c = {
            "title": "Comment Reports",
            "model_name": "Comment",
            "data": data,
            "schema": schema_comment_report,
            "reporting": True,
            "review_header": "Comment Reports",
            "review_description": "Take action on comments that have been reported by users.",
            "back_url": reverse("case_admin:comments"),
        }
        return render(request, "case-admin.html", c)

