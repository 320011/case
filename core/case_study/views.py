from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.core import serializers

from .forms import CaseStudyForm, CaseStudyTagForm, MedicalHistoryForm, MedicationForm  # , CaseTagForm
from .models import Tag, TagRelationship, CaseStudy, MedicalHistory, Medication, Attempt, Comment, CommentVote


@login_required
def start_new_case(request):
    case = CaseStudy.objects.create(created_by=request.user)
    return HttpResponseRedirect(
        reverse("cases:create-new-case", kwargs={"case_study_id": case.id}))


@login_required
def create_new_case(request, case_study_id):
    # returns object (case_study), and boolean specifying whether an object was created
    case_study, created = CaseStudy.objects.get_or_create(pk=case_study_id)
    relevant_tags = TagRelationship.objects.filter(case_study=case_study)  # return Tags for that case_study
    medical_histories = MedicalHistory.objects.filter(case_study=case_study)
    medications = Medication.objects.filter(case_study=case_study)
    # Check if the choice was in years format, if yes, integer division by 12.
    if case_study.age:
        if case_study.age_type == 'Y':
            case_study.age = case_study.age // 12
    if request.method == "POST":
        # Fixes mutable error
        request.POST = request.POST.copy()
        # obtain forms with fields populated from POST request
        case_study_form = CaseStudyForm(request.POST, instance=case_study)
        case_study_tag_form = CaseStudyTagForm(request.POST)
        medical_history_form = MedicalHistoryForm(request.POST)
        medication_form = MedicationForm(request.POST)

        # if user adds medical history
        if request.POST["submission_type"] == "medical_history":
            body = request.POST["body"]  # obtain medical history body
            if body:
                # get or create new medical history relationship in the database
                mhx, created = MedicalHistory.objects.get_or_create(body=body, case_study=case_study)
                if created:
                    messages.success(request, 'Medical History added!')
                else:
                    messages.error(request,
                                   'This medical history already exists. If it is a repeated condition, please include when the condition occured.')

            medical_history_form = MedicalHistoryForm(request.POST)
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "tags": relevant_tags,
                              "medical_histories": medical_histories,
                              "medications": medications,
                              # "case_study_question_form": case_study_question_form,
                              "case_study_tag_form": case_study_tag_form,
                              "medical_history_form": medical_history_form,
                              "medication_form": medication_form,
                          })

        # if user adds medication
        elif request.POST["submission_type"] == "medication":
            name = request.POST["name"]  # obtain medication name
            if name:
                # get or create new medication relationship in the database
                medication, created = Medication.objects.get_or_create(name=name, case_study=case_study)
                if created:
                    messages.success(request, 'Medication added!')
                else:
                    messages.error(request, 'This medication already exists.')
            medication_form = MedicationForm(request.POST)
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "tags": relevant_tags,
                              "medical_histories": medical_histories,
                              "medications": medications,
                              "case_study_tag_form": case_study_tag_form,
                              "medical_history_form": medical_history_form,
                              "medication_form": medication_form,
                          })
        # if user adds tag
        elif request.POST["submission_type"] == "tag" and request.POST["tag_choice"]:
            # Create a new tag relationship for this case study.
            tag = Tag.objects.get(pk=int(request.POST["tag_choice"]))  # get tag object for tag_choice
            # get or create new tag relationship in the database
            created_tag_relationship, created = TagRelationship.objects.get_or_create(tag=tag, case_study=case_study)
            if created:
                messages.success(request, 'Tag added!')
            else:
                messages.error(request, 'This tag already exists.')

            case_study_tag_form = CaseStudyTagForm()
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "tags": relevant_tags,
                              "medical_histories": medical_histories,
                              "medications": medications,
                              # "case_study_question_form": case_study_question_form,
                              "case_study_tag_form": case_study_tag_form,
                              "medical_history_form": medical_history_form,
                              "medication_form": medication_form,
                          })

        elif request.POST["submission_type"] == "save":
            # Checking for the type on submission, if years, store the value as months
            if request.POST['age_type'] == 'Y':
                request.POST['age'] = int(request.POST['age']) * 12
            if case_study_form.is_valid():
                case_study_form.save()
                # When page is re rendered, the value from the database is taken, so if years, render the correct value
                if request.POST['age_type'] == 'Y':
                    request.POST['age'] = int(request.POST['age']) // 12
                case_study_form = CaseStudyForm(request.POST, instance=case_study)
                messages.success(request, 'Case Study saved!')
                return render(request, "create_new_case.html",
                              {
                                  "case_study_form": case_study_form,
                                  "tags": relevant_tags,
                                  "medical_histories": medical_histories,
                                  "medications": medications,
                                  "case_study_tag_form": case_study_tag_form,
                                  "medical_history_form": medical_history_form,
                                  "medication_form": medication_form,
                              })
        elif request.POST["submission_type"] == "submit":
            if request.POST['age_type'] == 'Y':
                request.POST['age'] = int(request.POST['age']) * 12
            if case_study_form.is_valid():
                case_study_form.save()
                case_study.date_submitted = timezone.now()
                case_study.save()
                messages.success(request, 'Case Study created!')
                return HttpResponseRedirect(reverse('cases:view-case', args=[case_study.id]))
            else:
                if request.POST['age_type'] == 'Y':
                    request.POST['age'] = int(request.POST['age']) // 12
                case_study_form = CaseStudyForm(request.POST, instance=case_study)
                return render(request, "create_new_case.html",
                              {
                                  "case_study_form": case_study_form,
                                  "tags": relevant_tags,
                                  "medical_histories": medical_histories,
                                  "medications": medications,
                                  # "case_study_question_form": case_study_question_form,
                                  "case_study_tag_form": case_study_tag_form,
                                  "medical_history_form": medical_history_form,
                                  "medication_form": medication_form,
                              })
        else:
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "tags": relevant_tags,
                              "medical_histories": medical_histories,
                              "medications": medications,
                              "case_study_tag_form": case_study_tag_form,
                              "medical_history_form": medical_history_form,
                              "medication_form": medication_form,
                          })
    else:
        case_study_form = CaseStudyForm(instance=case_study)
        case_study_tag_form = CaseStudyTagForm()
        medical_history_form = MedicalHistoryForm()
        medication_form = MedicationForm()
    return render(request, "create_new_case.html",
                  {
                      "case_study_form": case_study_form,
                      "tags": relevant_tags,
                      "medical_histories": medical_histories,
                      "medications": medications,
                      "case_study_tag_form": case_study_tag_form,
                      "medical_history_form": medical_history_form,
                      "medication_form": medication_form,
                  })


@login_required
def view_case(request, case_study_id):
    case_study = CaseStudy.objects.get(pk=case_study_id)
    mhx = MedicalHistory.objects.filter(case_study=case_study)
    medications = Medication.objects.filter(case_study=case_study)
    tags = TagRelationship.objects.filter(case_study=case_study)
    total_average = case_study.get_average_score()
    user_average = case_study.get_average_score(user=request.user)
    user_attempts = len(Attempt.objects.filter(case_study=case_study, user=request.user))
    total_attempts = len(Attempt.objects.filter(case_study=case_study))
    if user_attempts >= 1:
        comments = Comment.objects.filter(case_study=case_study_id)
    c = {
        "attempts": {
            "total_average": total_average,
            "total_attempts": total_attempts,
            "user_average": user_average,
            "user_attempts": user_attempts
        },
        "case": case_study,
        "mhx": mhx,
        "medications": medications,
        "tags": tags,
        "comments":comments
    }
    return render(request, "view_case.html", c)


def validate_answer(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    choice = request.GET.get('choice', None)
    success = False
    # Get message
    if choice == case.answer:
        success = True
    message = "<strong>Correct Answer: " + case.answer + "</strong><br><em>" + case.get_answer_from_character(
        case.answer) + "</em><br>You answered incorrectly. Your answer was <strong>" + choice + "</strong>, " + case.get_answer_from_character(
        choice)
    if success:
        message = "<strong>Correct Answer: " + case.answer + "</strong><br><em>" + case.get_answer_from_character(
            case.answer) + "</em><br>You answered correctly."
    # Get attempts information
    Attempt.objects.create(user_answer=choice, case_study=case, user=request.user, attempt_date=timezone.now())
    total_average = case.get_average_score()
    user_average = case.get_average_score(user=request.user)
    user_attempts = len(Attempt.objects.filter(case_study=case, user=request.user))
    total_attempts = len(Attempt.objects.filter(case_study=case))
    # Get comments
    comments = Comment.objects.filter(case_study=case_study_id)
    comments_json = serializers.serialize('json', comments)
    data = {
        'attempts': {
            'total_average': total_average,
            'total_attempts': total_attempts,
            'user_average': user_average,
            'user_attempts': user_attempts
        },
        'success': success,
        'answer_message': message,
        'feedback': case.feedback,
        'comments': comments_json
    }
    return JsonResponse(data)

def submit_comment(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    comment_body = request.GET.get('comment_body', None)
    comment_is_anon = request.GET.get('comment_is_anon', None)
    # Create comment 
    comment = Comment.objects.create(comment=comment_body, case_study=case, user=request.user, is_anon=comment_is_anon, comment_date=timezone.now())
    comment_list = serializers.serialize('json', [comment])
    data = {
        'comments': comment_list
    }
    return HttpResponse(comment_list, content_type="text/json-comment-filtered" )

def test_view(request, case_study_id):
    case_study = CaseStudy.objects.get(pk=case_study_id)
    return render(request, "test_view.html")


def show_comments(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    user_attempts = len(Attempt.objects.filter(case_study=case, user=request.user))
    comments_json = "" 
    if user_attempts >= 1:
        comments = Comment.objects.filter(case_study=case_study_id)
        comments_json = serializers.serialize('json', comments)
    data = {
        'comments':comments_json
    }
    return JsonResponse(comments_json)