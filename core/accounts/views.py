from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import User
from .tokens import account_activation_token


@login_required
def view_profile(request):
    c = {
        "title": "Cases | My Profile",
         "user_cases": [
            {
                "title": "Case 1: XYZ",
                "description": "This is a cool case description provided by a user. "
                               "This is a cool case description provided by a user. "
                               "This is a cool case description provided by a user. "
                               "This is a cool case description provided by a user. "
                               "This is a cool case description provided by a user. "
                               "This is a cool case description provided by a user. "
                               "This is a cool case description provided by a user. ",
                "pass_rate": 75,
                "view_count": 565688,
                "patient_sex": "M",
                "patient_age": 86
            },
        ] * 5,
    }
    return render(request, 'profile-cases.html', c)


@login_required
def view_profile_results(request):
    c = {
        "title": "Results | My Profile",
    }
    return render(request, "profile-results.html", c)


def view_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            message = render_to_string('mail/email-activate-account.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                "protocol": request.is_secure() and "https" or "http"
            })
            email_subject = 'Activate Your Case Account'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            message = {'message': 
                'The activation link is sent to your email. Please confirm your email address to complete the registration.'}
            return render(request, 'activate-message.html', message)
    else:
        form = SignUpForm()
    c = {
        "title": "Sign Up | Case",
        "form": form
    }
    return render(request, 'auth-signup.html', c)


def view_activate(request):
    id = request.GET.get("id")
    token = request.GET.get("token")

    if id is None or token is None:
        return HttpResponseBadRequest()

    try:
        uid = force_text(urlsafe_base64_decode(id))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    c = {
        "message": "Activation link is invalid!"
    }

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        c["message"] = "Your account has been successfully activated."

    return render(request, 'activate-message.html', c)


