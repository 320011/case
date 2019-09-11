from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import UserSettingsForm, LogInForm, SignUpForm
from .models import User
from case_study.models import CaseStudy, Attempt, TagRelationship
from .tokens import account_activation_token
from .decorators import anon_required
from django.contrib import messages

@login_required
def view_profile(request):
    user = request.user
    attempts = Attempt.objects.filter(user=request.user).distinct().values('case_study').annotate(case_count=Count('case_study')).filter(case_count__gt=0).order_by('case_study')
    cases = CaseStudy.objects.filter(id__in=[item['case_study'] for item in attempts])

    total_average, user_average, user_attempts, total_attempts, tags = [], [], [], [], []
    for case in cases:
        total_average.append(case.get_average_score())
        user_average.append(case.get_average_score(user=request.user))
        user_attempts.append(len(Attempt.objects.filter(case_study=case, user=request.user)))
        total_attempts.append(len(Attempt.objects.filter(case_study=case)))
        tags.append(TagRelationship.objects.filter(case_study=case))

    cases = list(zip(cases, total_average, user_average, user_attempts, total_attempts, tags))

    total_score = sum([a*b for a,b in zip(user_average, user_attempts)])
    total_tries = sum(user_attempts)
    if total_tries == 0:
        overall_score = 'N/A'
    else:
        overall_score = float("{0:.2f}".format(total_score/total_tries))

    c = {
        'cases' : cases,
        'user' : user,
        'overall_score' : overall_score
    }
    return render(request, "profile-base.html", c)


@login_required
def view_profile_results(request):
    c = {
        "title": "Results | My Profile",
    }
    return render(request, "profile-results.html", c)


def view_login(request):
    if request.method == "POST":
        form = LogInForm(data = request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            dbuser = User.objects.filter(email=email)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
            elif user is None and dbuser:
                if dbuser.first().is_active == True:
                    m = 'The email or password entered is incorrect.'
                else:
                    m = 'Please confirm your email address to login.'
                messages.error(request,m)
            else:
                messages.error(request,'The email or password entered is incorrect.')
    else:
        form = LogInForm()
    
    c = {
        "form": form
    }
    return render(request, "auth-login.html", c)


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
                           "email address to complete "
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
