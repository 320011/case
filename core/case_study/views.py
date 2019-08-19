# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from .forms import CaseStudyForm, CaseStudyQuestionForm, MedicalHistoryForm, MedicationForm  # , CaseTagForm
from .models import Tag, TagRelationships, CaseStudy


def index(request):
    return HttpResponse("Hello, world. You're at the case study index.")


def start_new_case(request):
    case = CaseStudy.objects.create(created_by=request.user)
    return HttpResponseRedirect(
        reverse('create-new-case', kwargs={'case_study_id': case.id}))


def create_new_case(request, case_study_id):
    if request.method == 'POST':
        case_study_form = CaseStudyForm(request.POST)
        case_study_question_form = CaseStudyQuestionForm(request.POST)
        if case_study_form.is_valid() and case_study_question_form.is_valid():
            medical_history_form = MedicalHistoryForm(request.POST)
            medication_form = MedicationForm(request.POST)
            return # redirect('somewhere')
    else:
        case_study_form = CaseStudyForm()
        case_study_question_form = CaseStudyQuestionForm()
        medical_history_form = MedicalHistoryForm()
        medication_form = MedicationForm()
        # case_tag_form = CaseTagForm()
    return render(request, 'create_new_case.html',
                  {'case_study_form': case_study_form, 'case_study_question_form': case_study_question_form,
                   'medical_history_form': medical_history_form,
                   'medication_form': medication_form,
                   })  # , 'case_tag_form':case_tag_form})



    # return HttpResponse("Hello, world. yo!")
