from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.sessions.models import Session


class UserManager(BaseUserManager):
    """
    Defines a model manager for User model with email field
    """
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_tutor", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        es = email.split("@")
        extra_fields.setdefault("first_name", es[0])
        extra_fields.setdefault("last_name", es[1])
        extra_fields.setdefault("university", "UWA")
        extra_fields.setdefault("degree_commencement_year", 2019)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user class
    """
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    university = models.CharField(max_length=150, blank=True)
    degree_commencement_year = models.IntegerField(help_text="Year of pharmacy degree commencement", blank=True,
                                                   null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # whether this user is still active
    is_staff = models.BooleanField(default=False)  # whether this user can access the admin site
    is_tutor = models.BooleanField(default=False) # whether this user will appear as a tutor / lecturer on the site
    is_deleted = models.BooleanField(default=False)  # used to soft delete a model
    is_report_silenced = models.BooleanField(default=False)  # used to stop false report spam
    is_banned = models.BooleanField(default=False)  # used to ban a user from the site

    # Assigns the new Manager to the User model
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()

    def ban(self):
        # ban the user
        self.is_banned = True
        self.save()
        # log the user out
        for s in Session.objects.all():
            if int(s.get_decoded().get('_auth_user_id')) == self.id:
                s.delete()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
