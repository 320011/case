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


def view_404(request, exception):
    return render(request, "error.html", {
        "code": 404,
        "title": "Not Found",
        "message": "404: Not Found",
        "reason": "We were unable to find the page or resource that you requested"
    })


def view_500(request):
    return render(request, "error.html", {
        "code": 500,
        "title": "Internal Server Error",
        "message": "500: Internal Server Error",
        "reason": "Please contact the site administrators if this continues to occur"
    })


def view_400(request, exception):
    return render(request, "error.html", {
        "code": 400,
        "title": "Bad Request",
        "message": "400: Bad Request",
        "reason": "The request you submitted was invalid"
    })


def view_403(request, exception):
    return render(request, "error.html", {
        "code": 403,
        "title": "Permission Denied",
        "message": "403: Permission Denied",
        "reason": "You do not have the required permissions to access that resource"
    })
