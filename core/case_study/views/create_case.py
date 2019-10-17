from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta

from ..forms import CaseStudyForm, CaseStudyTagForm, MedicalHistoryForm, MedicationForm, OtherForm  # , CaseTagForm
from ..models import Tag, TagRelationship, CaseStudy, MedicalHistory, Medication, Attempt, Comment, Other, Question

from django.db.models import Q
@login_required
def start_new_case(request):
    draft_case_count = CaseStudy.objects.filter(created_by=request.user, case_state=CaseStudy.STATE_DRAFT).count()
    c = {
        "unsubmitted_count": draft_case_count
    }
    if draft_case_count == 0 or request.POST.get("create_new_case", False) == "true":
        case = CaseStudy.objects.create(created_by=request.user)
        return HttpResponseRedirect(
            reverse("cases:create-new-case", kwargs={"case_study_id": case.id}))
    else:
        return render(request, "create_case_landing.html", c)


@login_required
def unsubmitted_cases(request):
    draft_cases = CaseStudy.objects.filter(created_by=request.user, case_state=CaseStudy.STATE_DRAFT).order_by("-date_created")
    c = {
        "unsubmitted_cases": draft_cases
    }
    return render(request, "draft_cases.html", c)


@login_required
def delete_unsubmitted_case(request):
    case_id = request.GET.get('id', None)
    case_study = get_object_or_404(CaseStudy, pk=case_id)
    case_study.delete()
    success = True if not case_study.id else False
    data = {
        'success': success
    }
    return JsonResponse(data)


@login_required
def create_new_case(request, case_study_id):
    # returns object (case_study), and boolean specifying whether an object was created
    case_study = get_object_or_404(CaseStudy, pk=case_study_id, case_state=CaseStudy.STATE_DRAFT, created_by=request.user)
    # case has been submitted or pending review so it cannot be accessed again
    if case_study.case_state != CaseStudy.STATE_DRAFT:
        return HttpResponseNotFound()
        # return HttpResponseRedirect(reverse('cases:view-case', args=[case_study.id]))
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
        # -- Medical history --
        medical_histories = list(MedicalHistory.objects.filter(case_study=case_study).values_list("body", flat=True))
        medical_history_list = request.POST.getlist("medical-history-list")
        # Create new ones
        for medical_history in medical_history_list:
            if medical_history not in medical_histories:
                MedicalHistory.objects.create(body=medical_history, case_study=case_study)
        medical_histories = list(MedicalHistory.objects.filter(case_study=case_study).values_list("body", flat=True))
        # Delete ones that are removed
        for medical_history in medical_histories:
            if medical_history not in medical_history_list:
                MedicalHistory.objects.filter(body=medical_history, case_study=case_study).delete()
        # Obtain updated list of medical histories
        medical_histories = MedicalHistory.objects.filter(case_study=case_study)

        # -- Medication --
        medications = list(Medication.objects.filter(case_study=case_study).values_list("name", flat=True))
        medication_list = request.POST.getlist("medication-list")
        # Create new ones
        for medication in medication_list:
            if medication not in medications:
                Medication.objects.create(name=medication, case_study=case_study)
        medications = list(Medication.objects.filter(case_study=case_study).values_list("name", flat=True))
        # Delete ones that are removed
        for medication in medications:
            if medication not in medication_list:
                Medication.objects.filter(name=medication, case_study=case_study).delete()
        # Obtain updated list of medical histories
        medications = Medication.objects.filter(case_study=case_study)

        # -- Other --
        others = list(Other.objects.filter(case_study=case_study).values_list("other_body", flat=True))
        other_list = request.POST.getlist("other-list")
        # Create new ones
        for other in other_list:
            if other not in others:
                Other.objects.create(other_body=other, case_study=case_study)
        others = list(Other.objects.filter(case_study=case_study).values_list("other_body", flat=True))
        # Delete ones that are removed
        for other in others:
            if other not in other_list:
                Other.objects.filter(other_body=other, case_study=case_study).delete()
        # Obtain updated list of medical histories
        others = Other.objects.filter(case_study=case_study)

        # -- Tag --
        relevant_tags = TagRelationship.objects.filter(case_study=case_study)
        tag_list = request.POST.getlist("tag-list")
        # Create new ones
        for tag in tag_list:
            tag_object = get_object_or_404(Tag, pk=tag)
            if not TagRelationship.objects.filter(tag=tag_object, case_study=case_study).exists():
                TagRelationship.objects.create(tag=tag_object, case_study=case_study)
        relevant_tag_ids = TagRelationship.objects.filter(case_study=case_study).values_list("tag",flat=True)
        relevant_tags = []
        for relevant_tag in relevant_tag_ids:
            relevant_tags.append(relevant_tag)

        if request.POST["submission_type"] == "save":
            # Checking for the type on submission, if years, store the value as months
            if request.POST['age_type'] == 'Y' and request.POST['age'] != '':
                request.POST['age'] = int(request.POST['age']) * 12
            if case_study_form.is_valid():
                case_study_form.save()
                # When page is re rendered, the value from the database is taken, so if years, render the correct value
                if request.POST['age_type'] == 'Y' and request.POST['age'] != '':
                    request.POST['age'] = int(request.POST['age']) // 12
                case_study_form = CaseStudyForm(request.POST, instance=case_study)
                messages.success(request, 'Case Study saved!')
                return render(request, "create_new_case.html",
                              {
                                  "case_study_form": case_study_form,
                                  "relevant_tags": relevant_tags,
                                  "all_tags": all_tags,
                                  "medical_histories": medical_histories,
                                  "medications": medications,
                                  "others": others,
                                  "case_study": case_study,
                              })
        elif request.POST["submission_type"] == "submit":
            if request.POST['age_type'] == 'Y':
                age_raw = request.POST['age']
                if age_raw:
                    request.POST['age'] = int(age_raw) * 12
                else:
                    request.POST['age'] = None
            if case_study_form.is_valid():
                case_study_form = case_study_form.save(commit=False)
                case_study_form.case_state = CaseStudy.STATE_REVIEW
                case_study_form.save()
                messages.success(request, 'Case submitted for review. '
                                          'An admin will review your case before it is made public.')
                return HttpResponseRedirect(reverse('default'))
            else:
                if request.POST['age_type'] == 'Y':
                    age_raw = request.POST['age']
                    if age_raw:
                        request.POST['age'] = int(age_raw) // 12
                    else:
                        request.POST['age'] = None
                case_study_form = CaseStudyForm(request.POST, instance=case_study)
                return render(request, "create_new_case.html",
                              {
                                  "case_study_form": case_study_form,
                                  "relevant_tags": relevant_tags,
                                  "all_tags": all_tags,
                                  "medical_histories": medical_histories,
                                  "medications": medications,
                                  "others": others,
                                  "case_study":case_study,
                              })
        else:
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "relevant_tags": relevant_tags,
                              "all_tags": all_tags,
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
                      "relevant_tags": relevant_tags,
                      "all_tags": all_tags,
                      "medical_histories": medical_histories,
                      "medications": medications,
                      "others": others,
                      "case_study":case_study,
                  })
