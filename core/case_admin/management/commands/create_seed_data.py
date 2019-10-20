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
                "lastName" : "R", 
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
        
        test_cases = {
            {
                "id" : 1 ,
                "case_description" : "" 
            }
        }

        print("hello")