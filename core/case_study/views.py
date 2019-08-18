# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import (
    Tag,
    CaseStudy
)
from .forms import CaseStudyForm, CaseStudyQuestionForm, MedicalHistoryForm, MedicationForm #, CaseTagForm 
from django.contrib import messages

def index(request):
    return HttpResponse("Hello, world. You're at the case study index.")


def create_new_case(request):
    # cases = CaseStudy.objects.all()
    # print(cases)
    # c = {
    #     'cases': cases
    # }
    if request.method == 'POST':
        case_study_form = CaseStudyForm(request.POST)
        case_study_question_form = CaseStudyQuestionForm(request.POST)
        medical_history_form = MedicalHistoryForm(request.POST)
        medication_form = MedicationForm(request.POST)
        # case_tag_form = CaseTagForm(request.POST)
        # if form.is_valid():
        #     username = form.cleaned_data.get('username')
        #     messages.success(request, f'Account created for {username}!')
        #     return redirect('accounts-home')
    else:
        case_study_form = CaseStudyForm()
        case_study_question_form = CaseStudyQuestionForm()
        medical_history_form = MedicalHistoryForm()
        medication_form = MedicationForm()
        # case_tag_form = CaseTagForm()

    return render(request, 'create_new_case.html', { 'case_study_form': case_study_form, 'case_study_question_form':case_study_question_form,
     'medical_history_form':medical_history_form, 'medication_form':medication_form}) #, 'case_tag_form':case_tag_form})
    # return HttpResponse("Hello, world. yo!")
