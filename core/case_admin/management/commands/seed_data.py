from django.core.management.base import BaseCommand
from django.db.models.base import ObjectDoesNotExist
import sys
sys.path.append("....")
from case_study.models import Tag, TagRelationship, CaseStudy, MedicalHistory, Medication, Attempt, Comment, Other, Question
from accounts.models import User


class Command(BaseCommand):
    help = 'Create or delete seed data'

    def add_arguments(self, parser):
            parser.add_argument('action', type=str, help='Create or delete seed data')
            parser.add_argument('-a', '--action', type=str, help='Create or delete seed data', )

    def handle(self, *args, **kwargs):
        
        # Get action argument 
        action = kwargs['action']

        test_users = [
            {
                "id" : 1 , 
                "firstName" : "David" , 
                "lastName" : "D", 
                "email" : "david@example.com",
                "password" : "test123456789!"
            }, 
            {
                "id" : 2 , 
                "firstName" : "Jessie" , 
                "lastName" : "J", 
                "email" : "jess@example.com",
                "password" : "test123456789!"
            }, 
            {
                "id" : 3, 
                "firstName" : "Bobby" , 
                "lastName" : "B", 
                "email" : "bobby@example.com",
                "password" : "test123456789!"
            }, 
            {
                "id" : 4, 
                "firstName" : "Sam" , 
                "lastName" : "S", 
                "email" : "sam@example.com",
                "password" : "test123456789!"
            }
            , 
            {
                "id" : 5, 
                "firstName" : "Sally" , 
                "lastName" : "S", 
                "email" : "sally@example.com",
                "password" : "test123456789!"
            }
        ]

        if action == "create":
            # create test users 
            for test_user in test_users:
                try:
                    user = User.objects.get(email=test_user["email"])
                    print(test_user["email"] + " User has already been created")
                except ObjectDoesNotExist:
                    user = User.objects.create(email=test_user["email"])
                    user.first_name = test_user["firstName"]
                    user.last_name = test_user["firstName"]
                    user.is_active = True 
                    user.university = "UWA"
                    user.degree_commencement_year = 2019
                    user.set_password(test_user["password"]) 
                    user.save()
                    print("Created user " + test_user["email"] )

        if action == "delete":
            # delete test users 
            for test_user in test_users:
                try:
                    user = User.objects.get(email=test_user["email"]).delete()
                    print(test_user["email"] + " User has been deleted")
                except:
                    print("Could not find or delete user " + test_user["email"])
        
        
        # test questions
        test_questions = [
            {
                "id":1,
                "body": "test_What should you tell the patient?"
            },
            {
                "id":2,
                "body": "test_What dosage should you provide?"
            },
            {
                "id":3,
                "body": "test_Who should you refer this patient to?"
            },
        ]

        if action == "create":
            # create test questions 
            for test_question in test_questions:
                try:
                    # check if question has already been created
                    question = Question.objects.get(body=test_question["body"])
                    print("Question: '" + test_question["body"] + "' has already been created")
                except ObjectDoesNotExist:
                    question = Question.objects.create(body=test_question["body"])
                    print("Question: '" + test_question["body"] + "' has been created")
        
        if action == "delete":
            for test_question in test_questions:
                try:
                    question = Question.objects.get(body=test_question["body"]).delete()
                    print("Question: '" + test_question["body"] + "' has been deleted")
                except:
                    print("Could not delete question: '" + test_question["body"] + "'")

        # test tags
        test_tags = [
            {
                "id":1,
                "name": "test_Fever"
            },
            {
                "id":2,
                "name": "test_Cold"
            },
            {
                "id":3,
                "name": "test_Rash"
            },
        ]
        if action == "create":
            # create test questions 
            for test_tag in test_tags:
                try:
                    # check if question has already been created
                    tag = Tag.objects.get(name=test_tag["name"])
                    print("Tag: '" + test_tag["name"] + "' has already been created")
                except ObjectDoesNotExist:
                    question = Tag.objects.create(name=test_tag["name"])
                    print("Tag: '" + test_tag["name"] + "' has been created")
        
        if action == "delete":
            for test_tag in test_tags:
                try:
                    question = Tag.objects.get(name=test_tag["name"]).delete()
                    print("Tag: '" + test_tag["name"] + "' has been deleted")
                except:
                    print("Could not delete tag: '" + test_tag["name"] + "'")
        
        # test tags
        test_cases = [
            {
                "id":1,
                "created_by": "david@example.com",
                "case_state": "P",
                "height" : 180,
                "weight" : 60,
                "scr" : 1.5, 
                "age_type" : "Y",
                "age" : 45,
                "sex" : "M",
                "description" : "A patient shows up with a bleeding knee and cuts to arms.",
                "question" : "test_What should you tell the patient?",
                "answer_a" : "Nothing",
                "answer_b" : "I can't help you",
                "answer_c" : "Go to a hospital",
                "answer_d" : "Here's some medication for your cuts",
                "answer" : "D",
                "feedback" : "Be helpful",
            },
            {
                "id":2,
                "created_by": "sally@example.com",
                "case_state": "P",
                "height" : 160,
                "weight" : 60,
                "scr" : 2.0, 
                "age_type" : "Y",
                "age" : 30,
                "sex" : "F",
                "description" : "A patient shows up complaining pains to her belly.",
                "question" : "test_What should you tell the patient?",
                "answer_a" : "Nothing",
                "answer_b" : "I can't help you",
                "answer_c" : "Go to a hospital",
                "answer_d" : "Here's some medication for your tummy",
                "answer" : "D",
                "feedback" : "Be helpful",
            },
            {
                "id":3,
                "created_by": "bobby@example.com",
                "case_state": "P",
                "height" : 190,
                "weight" : 50,
                "scr" : 2.0, 
                "age_type" : "Y",
                "age" : 17,
                "sex" : "F",
                "description" : "A patient shows up complaining feeling faint.",
                "question" : "test_What should you tell the patient?",
                "answer_a" : "Nothing",
                "answer_b" : "I can't help you",
                "answer_c" : "Go to a hospital",
                "answer_d" : "Here's some medication for your faintness",
                "answer" : "C",
                "feedback" : "Patient is underweight",
            },
        ]


        if action == "create":
            # create test users 
            for test_case in test_cases:
                try:
                    case = CaseStudy.objects.get(description=test_case["description"])
                    print(test_case["description"] + " case has already been created")
                except ObjectDoesNotExist:
                    case = CaseStudy.objects.create(description=test_case["description"])
                    user = User.objects.get(email=test_user["email"])
                    case.created_by = user
                    case.case_state = test_case["case_state"]
                    case.height = test_case["height"]
                    case.weight = test_case["weight"]
                    case.scr = test_case["scr"]
                    case.age_type = test_case["age_type"]
                    case.age = test_case["age"]
                    case.sex = test_case["sex"]
                    case.description = test_case["description"]
                    case.answer_a = test_case["answer_a"]
                    case.answer_b = test_case["answer_b"]
                    case.answer_c = test_case["answer_c"]
                    case.answer_d = test_case["answer_d"]
                    case.answer = test_case["answer"]
                    case.feedback = test_case["feedback"]
                    case.save()
                    print("Created case " + test_case["description"] )
        
        if action == "delete":
            for test_case in test_cases:
                try:
                    case = CaseStudy.objects.get(description=test_case["description"]).delete()
                    print(test_case["description"] + " case has been deleted")
                except:
                   print("Could not delete: '" + test_case["description"] + "'")



        if action == "create":
            print("----- Create seed data complete -----")
        if action == "delete":
            print("----- Delete seed data complete -----")