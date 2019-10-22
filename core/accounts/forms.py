from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LogInForm(forms.Form):
    """
    Attributes added to customise for bootstrap
    """
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "email",
                "name": "email",
                "placeholder": "Email",
                "autofocus": "autofocus"
            }),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "name": "password",
                "placeholder": "Password"
            }
        ),
        label="Password"
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password"
        ]


class SignUpForm(UserCreationForm):
    """
    Attributes added to customise for bootstrap
    """
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "first_name",
                "placeholder": "First Name",
                "autofocus": "autofocus"
            }),
        label="First Name"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "last_name",
                "placeholder": "Last Name"
            }),
        label="Last Name"
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "email",
                "name": "email",
                "placeholder": "Email"
            }),
        label="Email"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "name": "password1",
                "placeholder": "Password"
            }
        ),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "name": "password2",
                "placeholder": "Confirm Password"
            }
        ),
        label="Confirm Password"
    )
    university = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "university",
                "placeholder": "University"
            }
        ),
        label="University"
    )
    degree_commencement_year = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "degree_commencement_year",
                "placeholder": "Pharmacy Degree Commencement Year"
            }
        ),
        label="Degree Commencement Year"
    )
    terms_accepted = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-control",
                "type": "checkbox",
                "name": "tos_accepted",
                "placeholder": ""
            }
        ),
        label="I understand and accept that any information I provide to UWA Pharmacy Case may be utilised in "
              "internal analytics that could include but is not limited to improving learning outcomes "
              "for the master of pharmacy course at UWA."
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "university",
            "degree_commencement_year"
        ]

class UserSettingsForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "first_name",
                "placeholder": "First Name"
            }),
        label="First Name"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "last_name",
                "placeholder": "Last Name"
            }),
        label="Last Name"
    )

    university = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "university",
                "placeholder": "University"
            }
        ),
        label="University"
    )
    degree_commencement_year = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "degree_commencement_year",
                "placeholder": "Pharmacy Degree Commencement Year"
            }
        ),
        label="Degree Commencement Year"
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "university",
            "degree_commencement_year"
        ]
