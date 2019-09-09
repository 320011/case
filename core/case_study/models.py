from django.db import models
# from django.contrib.auth.models import User
from datetime import datetime
from accounts.models import User


# blank=True means that the field is not required
class Question(models.Model):
    body = models.TextField()

    def __str__(self):
        return self.body


class Tag(models.Model):
    name = models.CharField(max_length=60, blank=False, unique=True, null=False)

    def __str__(self):
        return self.name


class CaseStudy(models.Model):
    YEARS = "Y"
    MONTHS = "M"
    AGE_CHOICES = [
        (YEARS, "Years"),
        (MONTHS, "Months")
    ]
    # Sex Choices
    MALE = "M"
    FEMALE = "F"
    SEX_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female")
    ]
    # Answer Choices
    ANSWER_A = "A"
    ANSWER_B = "B"
    ANSWER_C = "C"
    ANSWER_D = "D"
    ANSWER_CHOICES = [
        (ANSWER_A, "A"),
        (ANSWER_B, "B"),
        (ANSWER_C, "C"),
        (ANSWER_D, "D")
    ]
    # Processing information and settings
    date_created = models.DateTimeField(default=datetime.now)
    date_submitted = models.DateTimeField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=True)
    date_last_edited = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="created_by")
    last_edited_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="last_edited_user")
    is_deleted = models.BooleanField(default=False)
    # Case study fields
    height = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    scr = models.FloatField(null=True, blank=True)
    age_type = models.CharField(
        max_length=1,
        choices=AGE_CHOICES,
        default=YEARS
    )
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default=MALE,
        blank=True
    )
    description = models.TextField(null=True, blank=True)
    # Case Study Question and Answer
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer_a = models.TextField(null=True, blank=True)
    answer_b = models.TextField(null=True, blank=True)
    answer_c = models.TextField(null=True, blank=True)
    answer_d = models.TextField(null=True, blank=True)
    answer = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES,
        blank=True,
        null=True
    )
    feedback = models.TextField(null=True, blank=True)


class TagRelationship(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)

    def __str__(self):
        return "Tags {} as {}".format(str(self.case_study), str(self.tag))


class MedicalHistory(models.Model):
    body = models.TextField(null=True, blank=True)
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)

    def __str__(self):
        return self.body


class Medication(models.Model):
    name = models.TextField(null=True, blank=True)
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
