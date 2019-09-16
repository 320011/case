from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .forms import CaseStudyForm, CaseStudyTagForm, MedicalHistoryForm, MedicationForm  # , CaseTagForm
from .models import Tag, TagRelationship, CaseStudy, MedicalHistory, Medication, Attempt

from django.db.models import Count


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
        "tags": tags
    }
    return render(request, "view_case.html", c)


def validate_answer(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    choice = request.GET.get('choice', None)
    success = False
    if choice == case.answer:
        success = True
    message = "<strong>Correct Answer: " + case.answer + "</strong><br><em>" + case.get_answer_from_character(
        case.answer) + "</em><br>You answered incorrectly. Your answer was <strong>" + choice + "</strong>, " + case.get_answer_from_character(
        choice)
    if success:
        message = "<strong>Correct Answer: " + case.answer + "</strong><br><em>" + case.get_answer_from_character(
            case.answer) + "</em><br>You answered correctly."
    Attempt.objects.create(user_answer=choice, case_study=case, user=request.user, attempt_date=timezone.now())
    total_average = case.get_average_score()
    user_average = case.get_average_score(user=request.user)
    user_attempts = len(Attempt.objects.filter(case_study=case, user=request.user))
    total_attempts = len(Attempt.objects.filter(case_study=case))
    data = {
        'attempts': {
            'total_average': total_average,
            'total_attempts': total_attempts,
            'user_average': user_average,
            'user_attempts': user_attempts
        },
        'success': success,
        'answer_message': message,
        'feedback': case.feedback
    }
    return JsonResponse(data)


#small helper function
def get_or_none(req,get):
    out = ""
    if get.get(req) is not None:
        out = get.get(req)
    
    return out

@login_required
def search(request):


    get=request.GET
    cases = CaseStudy.objects
    cases=cases.filter()


    keywords=get.get("key_words")
    if keywords is not None and len(keywords) !=0:
        kw_list=keywords.split()
        for k in kw_list:
            cases=cases.filter(description__icontains=k)


    
    
    sex_choices = get.getlist('sex_choice')
    if len(sex_choices) != 0:
        sex_choices=sex_choices
        cases = cases.filter(sex__in=[s for s in sex_choices])

    mhxs = get.get("mhx")
    if mhxs is not None and len(mhxs) != 0:
        mhx_list = mhxs.split()
        for k in mhx_list:
            cases = cases.filter(medicalhistory__body__icontains=k)


    medicines = get.get("medication")
    if medicines is not None and len(medicines) != 0:
        medication_list = medicines.split()
        for k in medication_list:
            cases = cases.filter(medication__name__icontains=k)

    
    debug=[]
    tag_list=get.getlist('tag_choice')
    if len(tag_list) != 0:
        filter_ids = []
        for case in cases:
            case_tags = TagRelationship.objects.filter(case_study=case)
            for tag in case_tags:
                if tag.tag.name in tag_list:
                    filter_ids.append(case.id)   
        cases = cases.filter(id__in=[item for item in filter_ids])

    

    for case in cases:
        case_tags = TagRelationship.objects.filter(case_study=case)
        case.tags=case_tags


    #all tags
    tags = Tag.objects.filter()
    sexes =CaseStudy.SEX_CHOICES


    c={
        "tags": tags,
        "sexes": sexes,
        "get":get,

        'cases': cases,
        

        "key_words": get_or_none("key_words",get),
        "mhx":  get_or_none('mhx',get),
        "medication": get_or_none('medication',get),
        "sex_choices": get.getlist('sex_choice'),
        "tag_choices": get.getlist('tag_choice'),
    }
    
    # c={
    #     "case_study_form": case_study_form,
    #     "tags": relevant_tags,
    #     "medical_histories": medical_histories,
    #     "medications": medications,
    #     "case_study_tag_form": case_study_tag_form,
    #     "medical_history_form": medical_history_form,
    #     "medication_form": medication_form,
    # }

    return render(request,"search.html",c)
