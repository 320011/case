from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# blank=True means that the field is not required
class Question(models.Model):
    body = models.TextField()


class Tag(models.Model):
    name = models.CharField(max_length=60)


class CaseStudy(models.Model):
    # Years Choices
    YEARS = 'Y'
    MONTHS = 'M'
    AGE_CHOICES = [
        (YEARS, 'Years'),
        (MONTHS, 'Months')
    ]
    # Sex Choices
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    # Processing information and settings
    date_created = models.DateTimeField(default=datetime.now)
    date_submitted = models.DateTimeField(null=True)
    date_last_edited = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Don't use FK here to Users, use integer instead and check later, as on_delete can't be CASCADE
    last_edited_user = models.IntegerField(null=True)
    is_deleted = models.BooleanField(default=False)
    # Case study fields
    height = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    scr = models.FloatField(null=True)
    age_type = models.CharField(
        max_length=1,
        choices=AGE_CHOICES,
        default=YEARS
    )
    age = models.IntegerField(null=True)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default=MALE
    )
    description = models.TextField(null=True)
    # Case Study Question and Answer
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer_1 = models.TextField(null=True)
    answer_2 = models.TextField(null=True)
    answer_3 = models.TextField(null=True)
    answer_4 = models.TextField(null=True)
    feedback = models.TextField(null=True)


class TagRelationships(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)


class MedicalHistory(models.Model):
    body = models.TextField()
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)


class Medication(models.Model):
    name = models.TextField()
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)

