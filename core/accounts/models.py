from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.deconstruct import deconstructible
from os import path
import uuid

@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        return path.join(self.path, "%s.%s" % (uuid.uuid4().hex, ext))


class UserProfile(models.Model):
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name_first = models.CharField(max_length=20, default='')
    name_last = models.CharField(max_length=20, default='')
    avatar = models.ImageField(upload_to=PathAndRename('avatars/'), default='/static/img/profile-default.png')
    bio = models.CharField(max_length=160, blank=True, default='')
    gender = models.CharField(default='Male', max_length=20)
    dob = models.DateField(blank=True)
    study_commenced = models.DateField(blank=False, null=False)

    def __str__(self):
        return self.name_first + " " + self.name_last


# this code links our custom UserProfile model to the django User model
def create_user_profile(sender, **kwargs):
    UserProfile.objects.get_or_create(user=kwargs['instance'])
