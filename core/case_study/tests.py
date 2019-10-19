from django.test import TestCase

from .models import *
from accounts.models import User


# Unit tests for case_study module.

class CaseStudyTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="test@test.com")
        CaseStudy.objects.create(age=24, answer_a="a", answer_b="b", answer_c="c", answer_d="d", answer="D", height=175, weight=70, scr=3)
        CaseStudy.objects.create(age=24, sex=CaseStudy.FEMALE, age_type=CaseStudy.MONTHS, answer_a="a", answer_b="b",
                                 answer_c="c", answer_d="d", answer="C", height=175, weight=70)
        Attempt.objects.create(case_study_id=1, user_answer="A", user_id=1)
        Attempt.objects.create(case_study_id=1, user_answer="D", user_id=1)
        Attempt.objects.create(case_study_id=2, user_answer="C", user_id=1)

    def test_age_string(self):
        first_case = CaseStudy.objects.get(pk=1)
        second_case = CaseStudy.objects.get(pk=2)
        self.assertEquals(first_case.get_age_string(), "2-yo")
        self.assertEquals(second_case.get_age_string(), "24-mo")

    def test_age_in_words(self):
        first_case = CaseStudy.objects.get(pk=1)
        second_case = CaseStudy.objects.get(pk=2)
        self.assertEquals(first_case.get_age_in_words(), "two")
        self.assertEquals(second_case.get_age_in_words(), "twenty-four")

    def test_sex(self):
        first_case = CaseStudy.objects.get(pk=1)
        second_case = CaseStudy.objects.get(pk=2)
        self.assertEquals(first_case.get_sex(), "male")
        self.assertEquals(second_case.get_sex(), "female")

    def test_optionals(self):
        first_case = CaseStudy.objects.get(pk=1)
        second_case = CaseStudy.objects.get(pk=2)
        self.assertEquals(first_case.get_optionals(), "[175cm/70.0kg/3.0μmol/L SCr]")
        self.assertEquals(second_case.get_optionals(), "[175cm/70.0kg]")

    def test_answer_from_character(self):
        first_case = CaseStudy.objects.get(pk=1)
        second_case = CaseStudy.objects.get(pk=2)
        self.assertEquals(first_case.get_answer_from_character("A"), "a")
        self.assertEquals(second_case.get_answer_from_character("B"), "b")

    def test_average_score(self):
        first_case = CaseStudy.objects.get(pk=1)
        second_case = CaseStudy.objects.get(pk=2)
        self.assertEquals(first_case.get_average_score(), 50.0)
        self.assertEquals(second_case.get_average_score(), 100.0)
