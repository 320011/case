from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the case study index.")

def create_new_case(request):
    return HttpResponse("Create new case")
