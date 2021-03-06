# from django.contrib.auth.models import User
from datetime import datetime

from django.db import models
from num2words import num2words

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

    def get_average_score(self):
        total_sum = 0
        attempt_count = 0
        instances = TagRelationship.objects.filter(tag_id=self.id)
        if instances:
            for instance in instances:
                case = instance.case_study
                if case.get_average_score():
                    total_sum += case.get_average_score()
                attempt_count += Attempt.objects.filter(case_study_id=case.id).count()
            return {"score": total_sum/instances.count(), "attempts": attempt_count}
        return None


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
    # Case State Choices
    STATE_DRAFT = "D"
    STATE_REVIEW = "R"
    STATE_PUBLIC = "P"
    STATE_CHOICES = [
        (STATE_DRAFT, "D"),
        (STATE_REVIEW, "R"),
        (STATE_PUBLIC, "P"),
    ]
    # Processing information and settings
    date_created = models.DateTimeField(default=datetime.now, null=False)
    date_submitted = models.DateTimeField(null=True)
    is_anonymous = models.BooleanField(default=True, null=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_by")
    is_deleted = models.BooleanField(default=False, null=False)
    case_state = models.CharField(
        max_length=1,
        choices=STATE_CHOICES,
        default=STATE_DRAFT,
        blank=False,
        null=False
    )
    # Case study fields
    height = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    scr = models.FloatField(null=True, blank=True)
    age_type = models.CharField(
        max_length=1,
        choices=AGE_CHOICES,
        default=YEARS,
        blank=True
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
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
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

    def __str__(self):
        return "Case #{}".format(self.id)

    def get_age_string(self):
        if self.age_type == 'Y':
            if self.age:
                return str(self.age // 12) + '-yo'
            else:
                return ""
        return str(self.age) + '-mo'

    def get_age_in_words(self):
        if self.age_type == 'Y':
            if self.age:
                return num2words(self.age // 12)
            else:
                return ""
        return num2words(self.age)

    def get_sex(self):
        if self.sex == 'F':
            return 'female'
        return 'male'

    def get_optionals(self):
        if self.height:
            height = str(self.height) + 'cm'
        else:
            height = None
        if self.weight:
            weight = str(self.weight) + 'kg'
        else:
            weight = None
        if self.scr:
            scr = str(self.scr) + 'μmol/L SCr'
        else:
            scr = None
        optional_array = [height, weight, scr]
        optionals = ''
        if not height and not weight and not scr:
            return optionals
        else:
            output = '['
            for optional in optional_array:
                if optional:
                    output += optional + '/'
            if output.endswith('/'):
                output = output[:-1]
            output += ']'
            optionals = output
        return optionals

    # For Case View's AJAX Request
    def get_answer_from_character(self, character):
        if character == 'A':
            return self.answer_a
        elif character == 'B':
            return self.answer_b
        elif character == 'C':
            return self.answer_c
        elif character == 'D':
            return self.answer_d
        return None

    def get_average_score(self, user=None):
        attempts = len(Attempt.objects.filter(case_study=self))
        correct_attempts = len(Attempt.objects.filter(case_study=self, user_answer=self.answer))
        if user:
            attempts = len(Attempt.objects.filter(case_study=self, user=user))
            correct_attempts = len(Attempt.objects.filter(case_study=self, user_answer=self.answer, user=user))
        if attempts:
            return round(correct_attempts/attempts*100, 2)
        return None


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


class Other(models.Model):
    other_body = models.TextField(null=True, blank=True)
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)

    def __str__(self):
        return self.other_body


class Attempt(models.Model):
    user_answer = models.CharField(max_length=1, null=True)
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt_date = models.DateTimeField(null=True)


class Comment(models.Model):
    comment = models.TextField(null=True, blank=True)
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_anon = models.BooleanField(null=False, default=False)
    is_deleted = models.BooleanField(null=False, default=False)
    comment_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.comment


class CommentReport(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, related_name="report_comment")  # dont let people delete comments to hide from admins
    comment_author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="report_comment_author")
    report_author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="report_author")
    comment_body = models.TextField(null=False, blank=False)  # save a copy of the comment body at the time of the report so user cannot edit to hide
    comment_date = models.DateTimeField(null=False)
    report_date = models.DateTimeField(null=False)
    reason = models.TextField(null=False, blank=False)
    report_reviewed = models.BooleanField(null=False, default=False)


class Playlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    current_position = models.IntegerField(default=0)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    case_list = models.TextField(null=True)
    date_created = models.DateTimeField(default=datetime.now)

    def current_case(self):
        case_list = [int(case_id) for case_id in self.case_list.split(',')]
        return case_list[self.current_position]

    def next_case(self):
        case_list = [int(case_id) for case_id in self.case_list.split(',')]
        if self.current_position + 1 >= len(case_list):
            return None
        return case_list[self.current_position + 1]

    def previous_case(self):
        case_list = [int(case_id) for case_id in self.case_list.split(',')]
        if self.current_position - 1 < 0:
            return None
        return case_list[self.current_position - 1]

