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
import threading


def send_email_async(subject, content_subtype, template, template_context=None, from_email="UWA Pharmacy Case", to=None, cc=None, bcc=None):
    if not to:
        to = []
    if not cc:
        cc = []
    if not bcc:
        bcc = []
    if not template_context:
        template_context = {}

    def _send_mail_async(_subject, _content_subtype, _template, _template_context, _from_email, _to, _cc, _bcc):
        _message = render_to_string(_template, _template_context)
        _email = EmailMessage(_subject, _message, from_email=_from_email, to=_to, cc=_cc, bcc=_bcc)
        _email.content_subtype = _content_subtype
        _email.send()
    mailing_thread = threading.Thread(
        target=_send_mail_async,
        args=(subject, content_subtype, template, template_context, from_email, to, cc, bcc)
    )
    mailing_thread.start()


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

    # user's overall performance (average was calculated by each tries)
    total_score = sum([a*b for a,b in zip(user_average, user_attempts)])
    total_tries = sum(user_attempts)
    if total_tries == 0:
        overall_score = 'N/A'
    else:
        overall_score = float("{0:.2f}".format(total_score/total_tries))

    tag_filter, tag_score = "", 0
    # if the user filters the cases by tags or time, then the view needs to be updated
    if request.POST.get("filter_tag") and request.POST['filter_tag'] == 'All':
        pass
    elif request.POST.get("start_time") and request.POST.get("end_time"): # filter by both start and end dates
        start = request.POST['start_time']
        end = request.POST['end_time']
        # A day is added to the end date as the dates are not inclusive in __range
        end_date = datetime.strptime(end, "%Y-%m-%d")
        end_inclusive = end_date + timedelta(days=1) - timedelta(seconds=1)
        cases = CaseStudy.objects.filter(date_submitted__range=(start, end_inclusive))
    elif request.POST.get("start_time") and not request.POST.get("end_time"): # filter by only start date
        start = request.POST['start_time']
        cases = CaseStudy.objects.filter(date_submitted__gte=start)
    elif not request.POST.get("start_time") and request.POST.get("end_time"): # filter by only end date
        end = request.POST['end_time']
        # A day is added to make the selected end date inclusive
        end_date = datetime.strptime(end, "%Y-%m-%d")
        end_inclusive = end_date + timedelta(days=1) - timedelta(seconds=1)
        cases = CaseStudy.objects.filter(date_submitted__lte=end_inclusive)
    elif request.POST.get("filter_tag"):
        tag_filter = (request.POST['filter_tag']).replace('_', ' ').strip()
        filter_ids = []
        for case in cases:
            case_tags = TagRelationship.objects.filter(case_study=case)
            for tag in case_tags:
                if tag.tag.name == tag_filter:
                    filter_ids.append(case.id)
        cases = CaseStudy.objects.filter(id__in=[item for item in filter_ids])

        #calculate the score for this particular tag
        tag_average, tag_attempts = [], []
        for case in cases:
            tag_average.append(case.get_average_score(user=request.user))
            tag_attempts.append(len(Attempt.objects.filter(case_study=case, user=request.user)))

        total_tag_score = sum([a*b for a,b in zip(tag_average, tag_attempts)])
        total_tag_tries = sum(tag_attempts)
        tag_score = float("{0:.2f}".format(total_tag_score/total_tag_tries))


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
        'all_tags' : distinct_tags,
        'tag_filter' : tag_filter,
        'tag_score' : tag_score
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
        form = LogInForm(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            dbuser = User.objects.filter(email=email)

            if user is not None:
                if user.is_active and not user.is_deleted:
                    login(request, user)
                    return redirect('/')
                elif user.is_deleted:
                    messages.error(request, "This account has been closed. "
                                            "Please contact a member of staff if you believe this to be an error.")
            elif user is None and dbuser:
                if dbuser.first().is_active:
                    m = 'The email or password entered is incorrect.'
                else:
                    m = "Your account needs to be activated by a member of staff. " \
                        "You will receive an email when you have been approved and can log in."
                messages.error(request, m)
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

            # get all the admins' emails
            staff_emails = []
            staff = User.objects.filter(is_staff=True)
            for s in staff:
                staff_emails.append(s.email)

            send_email_async("Account Approval - {} ({})".format(user.first_name, user.email),
                             "html",
                             "mail/activate-account.html", {
                                 "user": user,
                                 "domain": get_current_site(request).domain,
                                 "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                 "token": account_activation_token.make_token(user),
                                 "protocol": request.is_secure() and "https" or "http",
                                 "success": False
                             },
                             bcc=staff_emails)
            c = {
                "header": "Account Confirmation",
                "message": "You will receive an email once your account has been activated by a staff member.\n"
                           "We appreciate your patience."
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
        "header": "Error",
        "message": "Activation link is invalid.",
        "error": "True"
    }

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        c = {
            "header": "Activation Successful",
            "message": "Name: {} {}\n"
                       "Email: {}".format(user.first_name, user.last_name, user.email),
        }

        #sends an email to the user whose account is activated
        send_email_async("Account Activated",
                         "html",
                         "mail/activate-account.html", {
                             "user": user,
                             "success": True,
                             "domain": get_current_site(request).domain,
                             "protocol": request.is_secure() and "https" or "http"
                         },
                         from_email='UWA Pharmacy Case',
                         to=[user.email])

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
            send_email_async("Password Changed",
                             "plain",
                             "mail/password-change.html", {
                                 "user": user,
                                 "domain": get_current_site(request).domain,
                                 "protocol": request.is_secure() and "https" or "http"
                             },
                             to=[request.user.email])
            c = {
                "message": "A confirmation message has been sent to your email."
            }
            return render(request, "change-password.html", c)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile-password.html', {
        'form': form
    })
