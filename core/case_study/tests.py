from django.test import TestCase
from .models import *

# Unit tests for case_study module.

class CaseStudyTestCase(TestCase):
    def setUp(self):
        CaseStudy.objects.create(age=24, answer_a="a", answer_b="b", answer_c="c", answer_d="d", answer="D")
        CaseStudy.objects.create(age=24, age_type=CaseStudy.MONTHS, answer_a="a", answer_b="b", answer_c="c", answer_d="d", answer="D")

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
