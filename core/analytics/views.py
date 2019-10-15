from django.shortcuts import render, get_object_or_404
import csv
from django.http import HttpResponse, JsonResponse
from case_study.models import Question, \
    Tag, CaseStudy, TagRelationship, \
    MedicalHistory, Medication, Other, Attempt, \
    Comment, CommentVote, CommentReport
from accounts.models import User
from .forms import TagForm


def export_queryset_csv(qs, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    csvw = csv.writer(response)
    header_done = False
    for e in qs:
        if not header_done:
            field_names = []
            for f in e._meta.fields:
                if f.name != "password":
                    field_names.append(f.name)
            csvw.writerow(field_names)
            header_done = True
        row_data = []
        for f in e._meta.fields:
            if f.name != "password":
                d = vars(e).get(f.attname, "")
                if d is None:
                    d = ""
                d = str(d).rstrip()
                row_data.append(d)
        csvw.writerow(row_data)
    return response


def view_landing(request):
    c = {"form": TagForm }
    return render(request, "analytics-landing.html", c)

def tag_performance(request):
    tag_id = request.GET.get('tag_id', None)
    tag = get_object_or_404(Tag, pk=tag_id)
    data = {}
    if tag.get_average_score():
        data = {
            'score': tag.get_average_score()["score"],
            'attempts': tag.get_average_score()["attempts"]
        }
    return JsonResponse(data)



def view_question(request):
    return export_queryset_csv(Question.objects.all(), "uwacase_questions.csv")


def view_tag(request):
    return export_queryset_csv(Tag.objects.all(), "uwacase_tags.csv")


def view_medicalhistory(request):
    return export_queryset_csv(MedicalHistory.objects.all(), "uwacase_medicalhistories.csv")


def view_comment(request):
    return export_queryset_csv(Comment.objects.all(), "uwacase_comments.csv")


def view_casestudy(request):
    return export_queryset_csv(CaseStudy.objects.all(), "uwacase_casestudies.csv")


def view_medication(request):
    return export_queryset_csv(Medication.objects.all(), "uwacase_medications.csv")


def view_commentvote(request):
    return export_queryset_csv(CommentVote.objects.all(), "uwacase_commentvotes.csv")


def view_tagrelationship(request):
    return export_queryset_csv(TagRelationship.objects.all(), "uwacase_tagrelationships.csv")


def view_other(request):
    return export_queryset_csv(Other.objects.all(), "uwacase_others.csv")


def view_commentreport(request):
    return export_queryset_csv(CommentReport.objects.all(), "uwacase_commentreports.csv")


def view_attempt(request):
    return export_queryset_csv(Attempt.objects.all(), "uwacase_attempts.csv")


def view_user(request):
    return export_queryset_csv(User.objects.all(), "uwacase_users.csv")

