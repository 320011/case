from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import SignUpForm
from .models import User
from .tokens import account_activation_token


class UserView(DetailView):
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email_subject = 'Activate Your Case Account'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return render(request, 'activate_confirmation.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))    #force_text instead of force_bytes
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been successfully activated')
    else:
        return HttpResponse('Activation link is invalid!')


def home(request):
    return render(request,'user/home.html')


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
