from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from case_admin.views.common import get_badge_counts


def index(request):
    if request.user.is_staff:
        return render(request, "index.html", {
            "badge_count_admin": get_badge_counts()["total"],
        })
    else:
        return render(request, "index.html")
