from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
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
from datetime import datetime, timedelta
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def view_profile(request):
    user = request.user
    attempts = Attempt.objects.filter(user=request.user).distinct().values('case_study').annotate(
            case_count=Count('case_study')).filter(case_count__gt=0).order_by('case_study')
    cases = CaseStudy.objects.filter(id__in=[item['case_study'] for item in attempts])

    # extract all the tags related to user's submitted cases and also the user averages and user
    # attempts to calculate the overall score of the user
    all_tags, all_tags_names, user_average, user_attempts = [], [], [], []
    for case in cases:
        all_tags.append(TagRelationship.objects.filter(case_study=case))
        user_average.append(case.get_average_score(user=request.user))
        user_attempts.append(len(Attempt.objects.filter(case_study=case, user=request.user)))
    
    # extracts all the tags names and only keeps the unique ones
    for tags in all_tags:
        for tag in tags:
            all_tags_names.append(tag.tag.name)
    distinct_tags = set(all_tags_names)

    # user's overall performance
    total_score = sum([a*b for a,b in zip(user_average, user_attempts)])
    total_tries = sum(user_attempts)
    if total_tries == 0:
        overall_score = 'N/A'
    else:
        overall_score = float("{0:.2f}".format(total_score/total_tries))

    # if the user filters the cases by tags or time, then the view needs to be updated
    if request.POST.get("filter_tag") and request.POST['filter_tag'] == 'All':
        pass
    elif request.POST.get("start_time") and request.POST.get("end_time"):
        start = request.POST['start_time']
        end = request.POST['end_time']
        # A day is added to the end date as the dates are not inclusive in __range
        end_date = datetime.strptime(end, "%Y-%m-%d")
        end_inclusive = end_date + timedelta(days=1) - timedelta(seconds=1)
        cases = CaseStudy.objects.filter(date_submitted__range=(start, end_inclusive))
    elif request.POST.get("filter_tag"):
        tag_filter = (request.POST['filter_tag']).replace('_', ' ').strip()
        filter_ids = []
        for case in cases:
            case_tags = TagRelationship.objects.filter(case_study=case)
            for tag in case_tags:
                if tag.tag.name == tag_filter:
                    filter_ids.append(case.id)
        cases = CaseStudy.objects.filter(id__in=[item for item in filter_ids])

    # all of these are calculated per case to be shown
    total_average, user_average, user_attempts, total_attempts, tags = [], [], [], [], []
    for case in cases:
        total_average.append(case.get_average_score())
        user_average.append(case.get_average_score(user=request.user))
        user_attempts.append(len(Attempt.objects.filter(case_study=case, user=request.user)))
        total_attempts.append(len(Attempt.objects.filter(case_study=case)))
        tags.append(TagRelationship.objects.filter(case_study=case))

    cases = list(zip(cases, total_average, user_average, user_attempts, total_attempts, tags))

    c = {
        'cases' : cases,
        'user' : user,
        'overall_score' : overall_score,
        'all_tags' : distinct_tags
    }
    return render(request, "profile-cases.html", c)


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


@login_required
def view_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password has been changed.')
            message = render_to_string("mail/password-change.html", {
                "user": user,
                "domain": get_current_site(request).domain,
                "protocol": request.is_secure() and "https" or "http"
            })
            email_subject = "Password Changed"
            print("this is hte email we will send the msg to:", request.user.email)
            email = EmailMessage(email_subject, message, to=[request.user.email])
            email.send()
            c = {
                "message": "A comfirmation message has been sent to your email."
            }
            return render(request, "change-password.html", c)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile-password.html', {
        'form': form
    })
