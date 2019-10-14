from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from case_study.models import Question, Tag, CaseStudy, TagRelationship, MedicalHistory, Medication, Other, Attempt, \
    Comment, CommentVote, CommentReport
from accounts.models import User


@login_required
def view_landing(request):
    c = {}
    return render(request, "analytics-landing.html", c)
