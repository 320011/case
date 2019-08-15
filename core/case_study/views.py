# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from case_study.models import (
    Tag,
    CaseStudy
)


def index(request):
    return HttpResponse("Hello, world. You're at the case study index.")


def create_new_case(request):
    cases = CaseStudy.objects.all()
    print(cases)
    c = {
        'cases': cases
    }
    return render(request, 'create_new_case.html', c)
    # return HttpResponse("Hello, world. yo!")
