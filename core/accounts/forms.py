from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


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
