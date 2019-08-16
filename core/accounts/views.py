from django.shortcuts import render


def profile(request, user_id):
    c = {}
    return render(request, "profile-cases.html", c)


def profile_results(request, user_id):
    c = {}
    return render(request, "profile-results.html", c)
