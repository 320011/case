from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from ..models import Tag, TagRelationship, CaseStudy, MedicalHistory, Medication, Attempt, Comment, Other, Question, CommentReport



@login_required
def view_case(request, case_study_id):
    case_study = get_object_or_404(CaseStudy, pk=case_study_id, case_state=CaseStudy.STATE_PUBLIC)
    mhx = MedicalHistory.objects.filter(case_study=case_study)
    medications = Medication.objects.filter(case_study=case_study)
    others = Other.objects.filter(case_study=case_study)
    tags = TagRelationship.objects.filter(case_study=case_study)
    total_average = case_study.get_average_score()
    user_average = case_study.get_average_score(user=request.user)
    user_attempts = Attempt.objects.filter(case_study=case_study, user=request.user).count()
    total_attempts = Attempt.objects.filter(case_study=case_study).count()
    comments = Comment.objects.filter(case_study=case_study_id, is_deleted=False).order_by("-comment_date")
    c = {
        "attempts": {
            "total_average": total_average,
            "total_attempts": total_attempts,
            "user_average": user_average,
            "user_attempts": user_attempts
        },
        "case": case_study,
        "mhx": mhx,
        "medications": medications,
        "others" : others,
        "tags": tags,
        "comments": comments
    }
    return render(request, "view_case.html", c)


@login_required
def validate_answer(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id, case_state=CaseStudy.STATE_PUBLIC)
    choice = request.GET.get('choice', None)
    success = False
    # Get message
    if choice == case.answer:
        success = True
    message = "<strong>Correct Answer: " + case.answer + "</strong><br><em>" + case.get_answer_from_character(
        case.answer) + "</em><br>You answered incorrectly. Your answer was <strong>" + choice + "</strong>, " + case.get_answer_from_character(
        choice)
    if success:
        message = "<strong>Correct Answer: " + case.answer + "</strong><br><em>" + case.get_answer_from_character(
            case.answer) + "</em><br>You answered correctly."
    # Get attempts information
    Attempt.objects.create(user_answer=choice, case_study=case, user=request.user, attempt_date=timezone.now())
    total_average = case.get_average_score()
    user_average = case.get_average_score(user=request.user)
    user_attempts = Attempt.objects.filter(case_study=case, user=request.user).count()
    total_attempts = Attempt.objects.filter(case_study=case).count()
    # Get comments
    comments = Comment.objects.filter(case_study=case_study_id)
    comments_json = serializers.serialize('json', comments)
    data = {
        'attempts': {
            'total_average': total_average,
            'total_attempts': total_attempts,
            'user_average': user_average,
            'user_attempts': user_attempts
        },
        'success': success,
        'answer_message': message,
        'feedback': case.feedback,
        'comments': comments_json
    }
    return JsonResponse(data)


@login_required
def submit_comment(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    body = request.GET.get('body', None)
    is_anon = request.GET.get('is_anon', None).capitalize()
    # Create comment
    if request.user.is_tutor:
        comment = Comment.objects.create(comment=body, case_study=case, user=request.user, is_anon=False,
                                        comment_date=timezone.now())
    else:
        comment = Comment.objects.create(comment=body, case_study=case, user=request.user, is_anon=is_anon,
                                        comment_date=timezone.now())
    data = {
        'comment': {
            'body': body,
            'date': timezone.now(),
            'is_anon': comment.is_anon == 'True'
        },
        'user': {
            'name': request.user.get_full_name(),
            'is_staff': request.user.is_staff,
            'is_tutor': request.user.is_tutor
        }
    }
    return JsonResponse(data)


@login_required
def submit_report(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    reasons = request.POST.get('report_reason', None)
    #create report
    report = CommentReport.objects.create(comment=comment,
        comment_author=comment.user, report_author=request.user,
        comment_body = comment.comment, comment_date = comment.comment_date,
        report_date=timezone.now(), reason=reasons, report_reviewed=False,
     )

    data = {

      'comment': {
        'author': report.comment_author.get_full_name(),
        'body': report.comment_body,
        'date': report.comment_date
      },

      'report': {
        'author': report.report_author.get_full_name(),
        'date': report.report_date,
        'reason': report.reason,
        'report_reviewed': False
      }

    }
    return JsonResponse(data)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.id_deleted = True
    comment.save()
    data = {}

    return JsonResponse(data)