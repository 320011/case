from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from case_admin.views.common import get_badge_counts
from case_study.models import CaseStudy


def index(request):
    draft_case_count = 0
    if request.user.is_authenticated:
        draft_case_count = CaseStudy.objects.filter(created_by=request.user, case_state=CaseStudy.STATE_DRAFT).count()

    if request.user.is_staff:
        return render(request, "index.html", {
            "badge_count_admin": get_badge_counts()["total"],
            "badge_count_new_case": draft_case_count,
        })
    else:
        return render(request, "index.html", {
            "badge_count_new_case": draft_case_count
        })
