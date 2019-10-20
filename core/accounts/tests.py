from django.core import mail
from django.test import TestCase

from .models import *

# Unit tests for User model

class AccountsTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="test@test.com", first_name="First", last_name="Last")
        User.objects.create(email="test2@test.com", first_name="First2", last_name="Last2")

    def test_full_name(self):
        first_user = User.objects.get(first_name="First")
        second_user = User.objects.get(first_name="First2")
        self.assertEquals(first_user.get_full_name(), "First Last")
        self.assertEquals(second_user.get_full_name(), "First2 Last2")

    def test_ban(self):
        u = User.objects.get(first_name="First")
        u.ban()
        self.assertEquals(u.is_banned, True)

    def test_send_email(self):
        u = User.objects.get(first_name="First")
        subject = "Test subject"
        message = "Test message"
        from_email = ["from@test.com"]
        u.email_user(subject, message, from_email)
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, "Test subject")
