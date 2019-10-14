from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .forms import CaseStudyForm, CaseStudyTagForm, MedicalHistoryForm, MedicationForm, OtherForm  # , CaseTagForm
from .models import Tag, TagRelationship, CaseStudy, MedicalHistory, Medication, Attempt, Comment, Other


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
    all_tags = Tag.objects.all()
    medical_histories = MedicalHistory.objects.filter(case_study=case_study)
    medications = Medication.objects.filter(case_study=case_study)
    others = Other.objects.filter(case_study=case_study)
    # Check if the choice was in years format, if yes, integer division by 12.
    if case_study.age:
        if case_study.age_type == 'Y':
            case_study.age = case_study.age // 12
    if request.method == "POST":
        # Fixes mutable error
        request.POST = request.POST.copy()
        # obtain forms with fields populated from POST request
        case_study_form = CaseStudyForm(request.POST, instance=case_study)

        if request.POST["submission_type"] == "save":
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
                                  "list_tags": all_tags, 
                                  "medical_histories": medical_histories,
                                  "medications": medications,
                                  "others": others,
                                  "case_study":case_study,
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
                                  "list_tags": all_tags, 
                                  "medical_histories": medical_histories,
                                  "medications": medications,
                                  "others": others,
                                  "case_study":case_study,
                              })
        else:
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "tags": relevant_tags,
                              "list_tags": all_tags, 
                              "medical_histories": medical_histories,
                              "medications": medications,
                              "others": others,
                              "case_study":case_study,
                          })
    else:
        case_study_form = CaseStudyForm(instance=case_study)
    return render(request, "create_new_case.html",
                  {
                      "case_study_form": case_study_form,
                      "tags": relevant_tags,
                      "list_tags": all_tags, 
                      "medical_histories": medical_histories,
                      "medications": medications,
                      "others": others,
                      "case_study":case_study,
                  })


@login_required
def add_medical_history(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    body = request.GET.get('body', None)
    # Create medical history  
    medical_history = MedicalHistory.objects.create(body=body, case_study=case)
    data = {
        'medical_history': {
            'body': body
        }
    }
    return JsonResponse(data)

@login_required
def add_medication(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    name = request.GET.get('name', None)
    # Create medication 
    medication = Medication.objects.create(name=name, case_study=case)
    data = {
        'medication': {
            'name': name
        }
    }
    return JsonResponse(data)

@login_required
def add_other(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    body = request.GET.get('body', None)
    # Create other 
    other = Other.objects.create(other_body=body, case_study=case)
    data = {
        'other': {
            'body': body
        }
    }
    return JsonResponse(data)

@login_required
def add_tag(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    tag_id = request.GET.get('tag_id', None)
    tag_name = request.GET.get('tag_name', None)
    tag_object = get_object_or_404(Tag, pk=tag_id) 
    success = False
    # Create tag  
    if TagRelationship.objects.filter(tag=tag_object, case_study=case).exists() == False:
        tag = TagRelationship.objects.create(tag=tag_object, case_study=case)
        success = True
        # Get updated tag id 
        tag_id = tag.id
    data = {
        'tag': {
            'id': tag_id, 
            'name': tag_name
        },
        'success': success
    }
    return JsonResponse(data)

@login_required
def view_case(request, case_study_id):
    case_study = get_object_or_404(CaseStudy, pk=case_study_id)
    mhx = MedicalHistory.objects.filter(case_study=case_study)
    medications = Medication.objects.filter(case_study=case_study)
    others = Other.objects.filter(case_study=case_study)
    tags = TagRelationship.objects.filter(case_study=case_study)
    total_average = case_study.get_average_score()
    user_average = case_study.get_average_score(user=request.user)
    user_attempts = Attempt.objects.filter(case_study=case_study, user=request.user).count()
    total_attempts = Attempt.objects.filter(case_study=case_study).count()
    comments = Comment.objects.filter(case_study=case_study_id, is_deleted=False).order_by("-comment_date")
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
        "others" : others, 
        "tags": tags,
        "comments": comments
    }
    return render(request, "view_case.html", c)

@login_required
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
    user_attempts = Attempt.objects.filter(case_study=case, user=request.user).count()
    total_attempts = Attempt.objects.filter(case_study=case).count()
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

@login_required
def submit_comment(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    body = request.GET.get('body', None)
    is_anon = request.GET.get('is_anon', None).capitalize()
    # Create comment 
    if request.user.is_tutor: 
        comment = Comment.objects.create(comment=body, case_study=case, user=request.user, is_anon=False,
                                        comment_date=timezone.now())
    else: 
        comment = Comment.objects.create(comment=body, case_study=case, user=request.user, is_anon=is_anon,
                                        comment_date=timezone.now())
    data = {
        'comment': {
            'body': body,
            'date': timezone.now(),
            'is_anon': comment.is_anon == 'True'
        },
        'user': {
            'name': request.user.get_full_name(),
            'is_staff': request.user.is_staff,
            'is_tutor': request.user.is_tutor
        }
    }
    return JsonResponse(data)
