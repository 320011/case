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

        if action == "create":
            print("----- Create seed data start -----")
        if action == "delete":
            print("----- Delete seed data start -----")

        if action == "delete":
            try:
                user = User.objects.all().delete()
                print("Users have been deleted")
            except:
                print("Users have already been delete")
            try:
                question = Question.objects.all().delete()
                print("Questions have been deleted")
            except:
                print("Questions have already been deleted")
            try:
                case = CaseStudy.objects.all().delete()
                print("Case Studies have been deleted")
            except:
                print("Case Studies have already been deleted")
            try:
                tag_relationship = TagRelationship.objects.all().delete()
                print("Tag relationships have been deleted")
            except:
                print("Tag relationships have already been deleted")
            try:
                question = Tag.objects.all().delete()
                print("Tags have been deleted")
            except:
                print("Tags have been already deleted")
            try:
                medical_history = MedicalHistory.objects.all().delete()
                print("Medical history have been deleted")
            except:
                print("Medical history have already been deleted")
            try:
                medication = Medication.objects.all().delete()
                print("Medication have been deleted")
            except:
                print("Medication have already been deleted")
            try:
                other = Other.objects.all().delete()
                print("Other have been deleted")
            except:
                print("Other have already been deleted")
            try:
                comment = Comment.objects.all().delete()
                print("Comment have been deleted")
            except:
                print("Comment have already been deleted")
            try:
                attempt = Attempt.objects.all().delete()
                print("Attempt have been deleted")
            except:
                print("Attempt have already been deleted")

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
                "firstName" : "Jess" , 
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
            for test_user in test_users:
                try:
                    user = User.objects.get(email=test_user["email"])
                    print(test_user["email"] + " User has already been created")
                except ObjectDoesNotExist:
                    user = User.objects.create(email=test_user["email"])
                    user.first_name = test_user["firstName"]
                    user.last_name = test_user["lastName"]
                    user.is_active = True 
                    user.university = "UWA"
                    user.degree_commencement_year = 2019
                    user.set_password(test_user["password"]) 
                    user.save()
                    print("Created user " + test_user["email"] )

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
            for test_question in test_questions:
                try:
                    question = Question.objects.get(body=test_question["body"])
                    print("Question: '" + test_question["body"] + "' has already been created")
                except ObjectDoesNotExist:
                    question = Question.objects.create(body=test_question["body"])
                    print("Question: '" + test_question["body"] + "' has been created")
        
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
            for test_tag in test_tags:
                try:
                    tag = Tag.objects.get(name=test_tag["name"])
                    print("Tag: '" + test_tag["name"] + "' has already been created")
                except ObjectDoesNotExist:
                    question = Tag.objects.create(name=test_tag["name"])
                    print("Tag: '" + test_tag["name"] + "' has been created")

        # test cases
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
                "description" : "with a bleeding knee and cuts to arms.",
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
                "description" : "complaining pains to her belly.",
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
                "description" : "complaining feeling faint.",
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
                    case.age = test_case["age"]
                    case.sex = test_case["sex"]
                    case.description = test_case["description"]
                    question = Question.objects.get(body=test_case["question"])
                    case.question = question
                    case.answer_a = test_case["answer_a"]
                    case.answer_b = test_case["answer_b"]
                    case.answer_c = test_case["answer_c"]
                    case.answer_d = test_case["answer_d"]
                    case.answer = test_case["answer"]
                    case.feedback = test_case["feedback"]
                    case.save()
                    print("Created case " + test_case["description"] )

        # test test_tag_relationships
        test_tag_relationships = [
            {
                "id":1,
                "tag": "test_Fever",
                "case": "complaining feeling faint."
            },
            {
                "id":2,
                "tag": "test_Cold",
                "case": "complaining feeling faint."
            },
            {
                "id":3,
                "tag": "test_Rash",
                "case": "with a bleeding knee and cuts to arms."
            },
            {
                "id":4,
                "tag": "test_Cold",
                "case": "complaining pains to her belly."
            },
        ]

        if action == "create":
            for test_tag_relationship in test_tag_relationships:
                try:
                    tag = Tag.objects.get(name=test_tag_relationship["tag"])
                    case = CaseStudy.objects.get(description=test_tag_relationship["case"])
                    tag_relationship = TagRelationship.objects.get(tag=tag, case_study=case)
                    print("Tag relationship: " + test_tag_relationship["tag"] + " with '" + test_tag_relationship["case"] +  "' has already been created")
                except ObjectDoesNotExist:
                    tag = Tag.objects.get(name=test_tag_relationship["tag"])
                    case = CaseStudy.objects.get(description=test_tag_relationship["case"])
                    tag_relationship = TagRelationship.objects.create(tag=tag, case_study=case)
                    print("Tag relationship: " + test_tag_relationship["tag"] + " with '" + test_tag_relationship["case"] + "' has been created")


        # test medical history
        test_medical_historys = [
            {
                "body" : "Family history of Huntington's diesease",
                "case" : "complaining feeling faint."
            }, 
            {
                "body" : "Asthma",
                "case" : "with a bleeding knee and cuts to arms."
            }, 
            {
                "body" : "Dislocated Shoulder",
                "case" : "with a bleeding knee and cuts to arms."
            }, 
            {
                "body" : "Asthma",
                "case" : "complaining pains to her belly."
            }, 
        ]

        if action == "create":
            for test_medical_history in test_medical_historys:
                try:
                    case = CaseStudy.objects.get(description=test_medical_history["case"])
                    medical_history = MedicalHistory.objects.get(body=test_medical_history["body"], case_study=case)
                    print("Medical history: " + test_medical_history["body"] + " with '" + test_medical_history["case"] +  "' has already been created")
                except ObjectDoesNotExist:
                    case = CaseStudy.objects.get(description=test_medical_history["case"])
                    medical_history = MedicalHistory.objects.create(body=test_medical_history["body"], case_study=case)
                    print("Medical history: " + test_medical_history["body"] + " with '" + test_medical_history["case"] +  "' has been created")
        
        # test medications
        test_medications = [
            {
                "name" : "Cortisol 50mg",
                "case" : "complaining feeling faint."
            }, 
            {
                "name" : "Panadol 500mg",
                "case" : "with a bleeding knee and cuts to arms."
            }, 
            {
                "name" : "Corex Cough Syrup",
                "case" : "complaining pains to her belly."
            }, 
            {
                "name" : "Panadol 500mg",
                "case" : "complaining pains to her belly."
            }, 
        ]

        if action == "create":
            for test_medication in test_medications:
                try:
                    case = CaseStudy.objects.get(description=test_medication["case"])
                    medication = Medication.objects.get(name=test_medication["name"], case_study=case)
                    print("Medication: " + test_medication["name"] + " with '" + test_medication["case"] +  "' has already been created")
                except ObjectDoesNotExist:
                    case = CaseStudy.objects.get(description=test_medication["case"])
                    medication = Medication.objects.create(name=test_medication["name"], case_study=case)
                    print("Medication: " + test_medication["name"] + " with '" + test_medication["case"] +  "' has been created")
        
        # test other
        test_others = [
            {
                "other_body" : "Currently seeing a specialist",
                "case" : "complaining feeling faint."
            }, 
        ]

        if action == "create":
            for test_other in test_others:
                try:
                    case = CaseStudy.objects.get(description=test_other["case"])
                    other = Other.objects.get(other_body=test_other["other_body"], case_study=case)
                    print("Other: " + test_other["other_body"] + " with '" + test_other["case"] +  "' has already been created")
                except ObjectDoesNotExist:
                    case = CaseStudy.objects.get(description=test_other["case"])
                    other = Other.objects.create(other_body=test_other["other_body"], case_study=case)
                    print("Other: " + test_other["other_body"] + " with '" + test_other["case"] +  "' has been created")
        
        # test comments 
        test_comments = [
            {
                "comment" : "Why is this answer D?",
                "case" : "complaining feeling faint.", 
                "user" : "bobby@example.com", 
                "comment_date": "2019-09-01T13:20:30",
            }, 
            {
                "comment" : "Because the patient has a history of huntington's diesease",
                "case" : "complaining feeling faint.", 
                "user" : "david@example.com",
                "comment_date": "2019-09-01T13:20:45",
            }, 
        ]

        if action == "create":
            for test_comment in test_comments:
                try:
                    case = CaseStudy.objects.get(description=test_comment["case"])
                    user = User.objects.get(email=test_comment["user"])
                    comment = Comment.objects.get(comment=test_comment["comment"], case_study=case, user=user, comment_date=test_comment["comment_date"])
                    print("Comment by: " + test_comment["user"] + "has already been created")
                except ObjectDoesNotExist:
                    case = CaseStudy.objects.get(description=test_comment["case"])
                    user = User.objects.get(email=test_comment["user"])
                    comment = Comment.objects.create(comment=test_comment["comment"], case_study=case, user=user, comment_date=test_comment["comment_date"])
                    print("Comment by: " + test_comment["user"] + "has been created")

        # test attempts
        test_attempts = [
            {
                "id":1,
                "user_answer": "A",
                "case": "complaining feeling faint.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-01T13:20:30",
            },
            {
                "id":2,
                "user_answer": "B",
                "case": "complaining feeling faint.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-02T13:20:30",
            },
            {
                "id":3,
                "user_answer": "C",
                "case": "complaining feeling faint.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-03T13:20:30",
            },
            {
                "id":4,
                "user_answer": "D",
                "case": "complaining feeling faint.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-04T13:20:30",
            },
            {
                "id":5,
                "user_answer": "D",
                "case": "complaining feeling faint.", 
                "user": "sally@example.com", 
                "attempt_date": "2019-09-02T13:20:30",
            },
            {
                "id":6,
                "user_answer": "D",
                "case": "complaining feeling faint.", 
                "user": "david@example.com", 
                "attempt_date": "2019-09-03T13:20:30",
            },
            {
                "id":7,
                "user_answer": "C",
                "case": "complaining feeling faint.", 
                "user": "jess@example.com", 
                "attempt_date": "2019-09-11T13:20:30",
            },
            {
                "id":8,
                "user_answer": "D",
                "case": "complaining feeling faint.", 
                "user": "jess@example.com", 
                "attempt_date": "2019-09-15T13:20:30",
            },
            {
                "id":9,
                "user_answer": "A",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-09T13:20:30",
            },
            {
                "id":10,
                "user_answer": "B",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-17T13:20:30",
            },
            {
                "id":11,
                "user_answer": "C",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-20T13:20:30",
            },
            {
                "id":12,
                "user_answer": "D",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-15T13:20:30",
            },
            {
                "id":13,
                "user_answer": "C",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "sally@example.com", 
                "attempt_date": "2019-09-07T13:20:30",
            },
            {
                "id":14,
                "user_answer": "D",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "sally@example.com", 
                "attempt_date": "2019-09-08T13:20:30",
            },
            {
                "id":15,
                "user_answer": "A",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "david@example.com", 
                "attempt_date": "2019-09-10T13:20:30",
            },
            {
                "id":16,
                "user_answer": "A",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "jess@example.com", 
                "attempt_date": "2019-09-11T13:20:30",
            },
            {
                "id":17,
                "user_answer": "D",
                "case": "complaining pains to her belly.", 
                "user": "jess@example.com", 
                "attempt_date": "2019-09-14T13:20:30",
            },
            {
                "id":18,
                "user_answer": "D",
                "case": "complaining pains to her belly.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-12T13:20:30",
            },
            {
                "id":19,
                "user_answer": "D",
                "case": "complaining pains to her belly.", 
                "user": "david@example.com", 
                "attempt_date": "2019-09-03T13:20:30",
            },
            {
                "id":20,
                "user_answer": "A",
                "case": "complaining pains to her belly.", 
                "user": "sally@example.com", 
                "attempt_date": "2019-09-06T13:20:30",
            },
        ]

        if action == "create":
            for test_attempt in test_attempts:
                try:
                    user = User.objects.get(email=test_attempt["user"])
                    case = CaseStudy.objects.get(description=test_attempt["case"])
                    attempt = Attempt.objects.get(user_answer=test_attempt["user_answer"],case_study=case,user=user,attempt_date=test_attempt["attempt_date"])
                    print("Attempt by: " + test_attempt["user"] + " for case '" + test_attempt["case"] +  "' has already been created")
                except ObjectDoesNotExist:
                    user = User.objects.get(email=test_attempt["user"])
                    case = CaseStudy.objects.get(description=test_attempt["case"])
                    attempt = Attempt.objects.create(user_answer=test_attempt["user_answer"],case_study=case,user=user,attempt_date=test_attempt["attempt_date"])
                    print("Attempt by: " + test_attempt["user"] + " for case '" + test_attempt["case"] +  "' has been created")
    
        if action == "create":
            print("----- Create seed data complete -----")
        if action == "delete":
            print("----- Delete seed data complete -----")