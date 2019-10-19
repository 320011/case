from django.test import TestCase

from .models import *
from accounts.models import User


# Unit tests for CaseStudy model

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

# Unit tests for Playlist model

class PlaylistTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="test@test.com")
        Playlist.objects.create(current_position=0, case_list="3,5,7,1", owner_id=1)
        Playlist.objects.create(current_position=3, case_list="8,5,7,4", owner_id=1)

    def test_current_case(self):
        first_playlist = Playlist.objects.get(pk=1)
        second_playlist = Playlist.objects.get(pk=2)
        self.assertEquals(first_playlist.current_case(), 3)
        self.assertEquals(second_playlist.current_case(), 4)

    def test_next_case(self):
        first_playlist = Playlist.objects.get(pk=1)
        second_playlist = Playlist.objects.get(pk=2)
        self.assertEquals(first_playlist.next_case(), 5)
        self.assertEquals(second_playlist.next_case(), None)

    def test_previous_case(self):
        first_playlist = Playlist.objects.get(pk=1)
        second_playlist = Playlist.objects.get(pk=2)
        self.assertEquals(first_playlist.previous_case(), None)
        self.assertEquals(second_playlist.previous_case(), 7)