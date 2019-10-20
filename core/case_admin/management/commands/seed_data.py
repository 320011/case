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
                "password" : "test123456789!", 
                "is_staff" : False,
                "commencement_year" : 2018,
            }, 
            {
                "id" : 2 , 
                "firstName" : "Jess" , 
                "lastName" : "J", 
                "email" : "jess@example.com",
                "password" : "test123456789!", 
                "is_staff" : False,
                "commencement_year" : 2019,
            }, 
            {
                "id" : 3, 
                "firstName" : "Bobby" , 
                "lastName" : "B", 
                "email" : "bobby@example.com",
                "password" : "test123456789!", 
                "is_staff" : False,
                "commencement_year" : 2018,
            }, 
            {
                "id" : 4, 
                "firstName" : "Sam" , 
                "lastName" : "S", 
                "email" : "sam@example.com",
                "password" : "test123456789!", 
                "is_staff" : False,
                "commencement_year" : 2018,
            }
            , 
            {
                "id" : 5, 
                "firstName" : "Sally" , 
                "lastName" : "S", 
                "email" : "sally@example.com",
                "password" : "test123456789!", 
                "is_staff" : False,
                "commencement_year" : 2018,

            }, 
            {
                "id" : 6, 
                "firstName" : "AdminTest" , 
                "lastName" : "AdminTest", 
                "email" : "admin@example.com",
                "password" : "test123456789!", 
                "is_staff" : True,
                "commencement_year" : 2018,
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
                    user.degree_commencement_year = test_user["commencement_year"]
                    user.set_password(test_user["password"]) 
                    user.is_staff = test_user["is_staff"]
                    user.save()
                    print("Created user " + test_user["email"] )

        # test questions
        test_questions = [
            {
                "id":1,
                "body": "What should you tell the patient?"
            },
            {
                "id":2,
                "body": "What dosage should you provide?"
            },
            {
                "id":3,
                "body": "Who should you refer this patient to?"
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
                "name": "Fever"
            },
            {
                "id":2,
                "name": "Cold"
            },
            {
                "id":3,
                "name": "Rash"
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
                "created_by": "sally@example.com",
                "case_state": "P",
                "height" : 180,
                "weight" : 60,
                "scr" : 1.5, 
                "age_type" : "Y",
                "age" : 540,
                "sex" : "M",
                "description" : "with a bleeding knee and cuts to arms.",
                "question" : "What dosage should you provide?",
                "answer_a" : "Nothing",
                "answer_b" : "I can't help you",
                "answer_c" : "Go to a hospital",
                "answer_d" : "Here's some medication for your cuts",
                "answer" : "D",
                "feedback" : "Be helpful",
                "date_created" : "2019-09-01T08:20:30",
            },
            {
                "id":2,
                "created_by": "sally@example.com",
                "case_state": "P",
                "height" : 160,
                "weight" : 60,
                "scr" : 2.0, 
                "age_type" : "Y",
                "age" : 360,
                "sex" : "F",
                "description" : "complaining pains to her belly.",
                "question" : "What should you tell the patient?",
                "answer_a" : "Nothing",
                "answer_b" : "I can't help you",
                "answer_c" : "Go to a hospital",
                "answer_d" : "Here's some medication for your tummy",
                "answer" : "D",
                "feedback" : "Be helpful",
                "date_created" : "2019-08-30T15:20:30",
            },
            {
                "id":3,
                "created_by": "david@example.com",
                "case_state": "P",
                "height" : 190,
                "weight" : 50,
                "scr" : 2.0, 
                "age_type" : "Y",
                "age" : 204,
                "sex" : "F",
                "description" : "complaining feeling faint.",
                "question" : "Who should you refer this patient to?",
                "answer_a" : "Nothing",
                "answer_b" : "I can't help you",
                "answer_c" : "Go to a hospital",
                "answer_d" : "Here's some medication for your faintness",
                "answer" : "D",
                "feedback" : "Patient is underweight",
                "date_created" : "2019-08-25T10:20:30",
            },
        ]


        if action == "create":
            for test_case in test_cases:
                try:
                    case = CaseStudy.objects.get(description=test_case["description"])
                    print(test_case["description"] + " case has already been created")
                except ObjectDoesNotExist:
                    case = CaseStudy.objects.create(description=test_case["description"])
                    case.created_by = User.objects.get(email=test_case["created_by"])
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
                    case.date_created = test_case["date_created"]
                    case.save()
                    print("Created case " + test_case["description"] )

        # test test_tag_relationships
        test_tag_relationships = [
            {
                "id":1,
                "tag": "Fever",
                "case": "complaining feeling faint."
            },
            {
                "id":2,
                "tag": "Cold",
                "case": "complaining feeling faint."
            },
            {
                "id":3,
                "tag": "Rash",
                "case": "with a bleeding knee and cuts to arms."
            },
            {
                "id":4,
                "tag": "Cold",
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
                "attempt_date": "2019-09-01T09:20:30",
            },
            {
                "id":2,
                "user_answer": "B",
                "case": "complaining feeling faint.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-02T09:20:30",
            },
            {
                "id":3,
                "user_answer": "C",
                "case": "complaining feeling faint.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-03T10:20:30",
            },
            {
                "id":4,
                "user_answer": "D",
                "case": "complaining feeling faint.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-04T11:20:30",
            },
            {
                "id":5,
                "user_answer": "D",
                "case": "complaining feeling faint.", 
                "user": "sally@example.com", 
                "attempt_date": "2019-09-02T12:20:30",
            },
            {
                "id":6,
                "user_answer": "D",
                "case": "complaining feeling faint.", 
                "user": "david@example.com", 
                "attempt_date": "2019-09-03T16:20:30",
            },
            {
                "id":7,
                "user_answer": "C",
                "case": "complaining feeling faint.", 
                "user": "jess@example.com", 
                "attempt_date": "2019-09-11T20:20:30",
            },
            {
                "id":8,
                "user_answer": "D",
                "case": "complaining feeling faint.", 
                "user": "jess@example.com", 
                "attempt_date": "2019-09-15T21:20:30",
            },
            {
                "id":9,
                "user_answer": "A",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-09T14:20:30",
            },
            {
                "id":10,
                "user_answer": "B",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-17T15:20:30",
            },
            {
                "id":11,
                "user_answer": "C",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-20T14:20:30",
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
                "attempt_date": "2019-09-07T20:20:30",
            },
            {
                "id":14,
                "user_answer": "D",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "sally@example.com", 
                "attempt_date": "2019-09-08T10:20:30",
            },
            {
                "id":15,
                "user_answer": "A",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "david@example.com", 
                "attempt_date": "2019-09-10T11:20:30",
            },
            {
                "id":16,
                "user_answer": "D",
                "case": "with a bleeding knee and cuts to arms.", 
                "user": "jess@example.com", 
                "attempt_date": "2019-09-11T12:20:30",
            },
            {
                "id":17,
                "user_answer": "D",
                "case": "complaining pains to her belly.", 
                "user": "jess@example.com", 
                "attempt_date": "2019-09-14T14:20:30",
            },
            {
                "id":18,
                "user_answer": "D",
                "case": "complaining pains to her belly.", 
                "user": "bobby@example.com", 
                "attempt_date": "2019-09-12T15:20:30",
            },
            {
                "id":19,
                "user_answer": "D",
                "case": "complaining pains to her belly.", 
                "user": "david@example.com", 
                "attempt_date": "2019-09-03T09:20:30",
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