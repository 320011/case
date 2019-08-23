from django.shortcuts import renderv

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    c = {}
    return render(request, "index.html", c)
