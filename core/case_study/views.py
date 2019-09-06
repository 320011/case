from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .forms import CaseStudyForm, CaseStudyTagForm, MedicalHistoryForm, MedicationForm  # , CaseTagForm
from .models import Tag, TagRelationship, CaseStudy, MedicalHistory, Medication


@login_required
def start_new_case(request):
    case = CaseStudy.objects.create(created_by=request.user)
    return HttpResponseRedirect(
        reverse("cases:create-new-case", kwargs={"case_study_id": case.id}))


@login_required
def create_new_case(request, case_study_id):
    # returns object (case_study), and boolean specifiying whether an object was created
    case_study, created = CaseStudy.objects.get_or_create(pk=case_study_id)
    relevant_tags = TagRelationship.objects.filter(case_study=case_study)  # return Tags for that case_study
    medical_histories = MedicalHistory.objects.filter(case_study=case_study)
    medications = Medication.objects.filter(case_study=case_study)
    message = {"content": "", "type": ""}
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
                    message["content"] = "Medical history added!"
                    message["type"] = "success"
                else:
                    message["content"] = "This medical history already exists. " \
                                         "If it is a repeated condition, please " \
                                         "include when the condition occured."
                    message["type"] = "danger"

            medical_history_form = MedicalHistoryForm(request.POST)
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "message": message,
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
                    message["content"] = "Medication added!"
                    message["type"] = "success"
                else:
                    message["content"] = "This medication already exists."
                    message["type"] = "danger"

            medication_form = MedicationForm(request.POST)
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "message": message,
                              "tags": relevant_tags,
                              "medical_histories": medical_histories,
                              "medications": medications,
                              # "case_study_question_form": case_study_question_form,
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
                message["content"] = "Tag added!"
                message["type"] = "success"
            else:
                message["content"] = "This tag already exists."
                message["type"] = "danger"

            case_study_tag_form = CaseStudyTagForm()
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "message": message,
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
                message["content"] = "Case Study Saved!"
                message["type"] = "success"
                return render(request, "create_new_case.html",
                              {
                                  "case_study_form": case_study_form,
                                  "tags": relevant_tags,
                                  "message": message,
                                  "medical_histories": medical_histories,
                                  "medications": medications,
                                  # "case_study_question_form": case_study_question_form,
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
                              # "case_study_question_form": case_study_question_form,
                              "case_study_tag_form": case_study_tag_form,
                              "medical_history_form": medical_history_form,
                              "medication_form": medication_form,
                          })
    else:
        case_study_form = CaseStudyForm(instance=case_study)
        # case_study_question_form = CaseStudyQuestionForm()
        case_study_tag_form = CaseStudyTagForm()
        medical_history_form = MedicalHistoryForm()
        medication_form = MedicationForm()
        # case_tag_form = CaseTagForm()
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


@login_required
def view_case(request, case_study_id):
    case_study = CaseStudy.objects.get(pk=case_study_id)
    mhx = MedicalHistory.objects.filter(case_study=case_study)
    tags = TagRelationship.objects.filter(case_study=case_study)
    print(mhx)
    c = {
        "case": case_study,
        "mhx": mhx,
        "tags": tags
    }
    return render(request, "view_case.html", c)
