from django.shortcuts import render


def profile(request, user_id):
    c = {
        "user_cases": [
            {
                "title": "Case 1: XYZ",
                "description": "This is a cool case description provided by a user. It is pretty long. It just doesnt stop does it.",
                "pass_rate": 0.75,
                "view_count": 565688,
                "patient_sex": "M",
                "patient_age": 86
            },
        ] * 5
    }
    return render(request, "profile-cases.html", c)


def profile_results(request, user_id):
    c = {}
    return render(request, "profile-results.html", c)
