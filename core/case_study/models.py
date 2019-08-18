from django.db import models
from accounts.models import User


# blank=True means that the field is not required
class Question(models.Model):
    body = models.TextField(help_text='Question text body')


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
    date_submitted = models.DateTimeField(null=True, blank=True)
    date_last_edited = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Don't use FK here to Users, use integer instead and check later, as on_delete can't be CASCADE
    last_edited_user = models.IntegerField(blank=True)
    is_deleted = models.BooleanField(default=False)
    # Case study fields
    height = models.IntegerField(blank=True)
    weight = models.FloatField(blank=True)
    scr = models.FloatField(blank=True)
    age_type = models.CharField(
        max_length=1,
        choices=AGE_CHOICES,
        default=YEARS
    )
    age = models.IntegerField()
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default=MALE
    )
    description = models.TextField(help_text='Description for case study scenario.')
    # Case Study Question and Answer
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_1 = models.TextField(help_text='Answer 1')
    answer_2 = models.TextField(help_text='Answer 2')
    answer_3 = models.TextField(help_text='Answer 3')
    answer_4 = models.TextField(help_text='Answer 4')
    feedback = models.TextField(help_text='Case study creator feedback')


class TagRelationships:
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class MedicalHistory(models.Model):
    body = models.TextField(help_text='Medical history information')
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)


class Medication(models.Model):
    name = models.TextField(help_text='Medication Name')
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)



