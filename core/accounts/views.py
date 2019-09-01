from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from .forms import UserSettingsForm
from .models import User
from .tokens import account_activation_token
from .decorators import anon_required
from django.contrib import messages

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
    return render(request, "profile-cases.html", c)


@login_required
def view_profile_results(request):
    c = {
        "title": "Results | My Profile",
    }
    return render(request, "profile-results.html", c)


@anon_required
def view_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            message = render_to_string("mail/activate-account.html", {
                "user": user,
                "domain": get_current_site(request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
                "protocol": request.is_secure() and "https" or "http"
            })
            email_subject = "Activate Your Case Account"
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            c = {
                "message": "An activation link has been "
                           "sent to {}. Please confirm your "
                           "email address to completed "
                           "registration.".format(to_email)
            }
            return render(request, "activate-message.html", c)
    else:
        form = SignUpForm()

    c = {
        "title": "Sign Up | Case",
        "form": form
    }
    return render(request, "auth-signup.html", c)


def view_activate(request):
    uid = request.GET.get("id")
    token = request.GET.get("token")

    if uid is None or token is None:
        return HttpResponseBadRequest()

    try:
        user_id = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    c = {
        "message": "Activation link is invalid."
    }

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        c["message"] = "Your account has been successfully activated."

    return render(request, "activate-message.html", c)


@login_required
def view_settings(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account details have been updated!')
            return render(request, "profile-settings.html", {'form': form})
    else:
        form = UserSettingsForm(instance=request.user)
    return render(request, "profile-settings.html", {'form': form})
