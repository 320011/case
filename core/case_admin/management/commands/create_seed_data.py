from django.core.management.base import BaseCommand
import sys
sys.path.append("....")
from case_study.models import Tag, TagRelationship, CaseStudy, MedicalHistory, Medication, Attempt, Comment, Other, Question
from accounts.models import User


class Command(BaseCommand):
    help = 'Create seed data'

    def handle(self, *args, **kwargs):
        test_users = {
            {
                "id" : 1 , 
                "firstName" : "David" , 
                "lastName" : "D", 
                "email" : "david@example.com",
                "password" : "test123456789!"
            } , 
            {
                "id" : 2 , 
                "firstName" : "Jessie" , 
                "lastName" : "J", 
                "email" : "jess@example.com",
                "password" : "test123456789!"
            } 
        }

        # create test users 
        for test_user in test_users:
            try:
                user = User.objects.get(email=test_user.email)
            except ObjectDoesNotExist:
                user = User.objects.create(email=test_user.email)
                user.first_name = test_user.firstName
                user.last_name = test_user.firstName
                user.is_active = True 
                user.university = "UWA"
                user.degree_commencement_year = 2019
                # user.set_password(test_user.password) 
                user.save()
                
        print("hello")