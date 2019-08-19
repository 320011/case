# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .forms import CaseStudyForm, CaseStudyTagForm, MedicalHistoryForm, MedicationForm  # , CaseTagForm
from .models import Tag, TagRelationships, CaseStudy, MedicalHistory, Medication


def index(request):
    return HttpResponse("Hello, world. You're at the case study index.")


def start_new_case(request):
    case = CaseStudy.objects.create(created_by=request.user)
    return HttpResponseRedirect(
        reverse('cases:create-new-case', kwargs={'case_study_id': case.id}))


def create_new_case(request, case_study_id):
    case_study, created = CaseStudy.objects.get_or_create(
        pk=case_study_id)  # returns object (case_study), and boolean specifiying whether an object was created
    relevant_tags = TagRelationships.objects.filter(case_study=case_study)  # return Tags for that case_study
    medical_historys = MedicalHistory.objects.filter(case_study=case_study)
    medications = Medication.objects.filter(case_study=case_study)
    if request.method == 'POST':
        print(request.POST)
        # obtain forms with fields populated from POST request
        case_study_form = CaseStudyForm(request.POST, instance=case_study)
        # case_study_question_form = CaseStudyQuestionForm(request.POST) 
        case_study_tag_form = CaseStudyTagForm(request.POST)
        medical_history_form = MedicalHistoryForm(request.POST)
        medication_form = MedicationForm(request.POST)

        # if user adds medical history 
        if request.POST['submission_type'] == 'medical_history':
            body = request.POST['body']  # obtain medical history body
            MedicalHistory.objects.get_or_create(body=body,
                                                 case_study=case_study)  # get or create new medical history relationship in the database

            medical_history_form = MedicalHistoryForm(request.POST)
            print(medical_history_form.is_valid())
            return render(request, 'create_new_case.html',
                          {'case_study_form': case_study_form,
                           'tags': relevant_tags,
                           'medical_historys': medical_historys,
                           'medications': medications,
                           # 'case_study_question_form': case_study_question_form,
                           'case_study_tag_form': case_study_tag_form,
                           'medical_history_form': medical_history_form,
                           'medication_form': medication_form,
                           })

        # if user adds medication
        elif request.POST['submission_type'] == 'medication':
            name = request.POST['name']  # obtain medication name
            Medication.objects.get_or_create(name=name,
                                             case_study=case_study)  # get or create new medication relationship in the database

            medication_form = MedicationForm(request.POST)
            print(medication_form.is_valid())
            return render(request, 'create_new_case.html',
                          {'case_study_form': case_study_form,
                           'tags': relevant_tags,
                           'medical_historys': medical_historys,
                           'medications': medications,
                           # 'case_study_question_form': case_study_question_form,
                           'case_study_tag_form': case_study_tag_form,
                           'medical_history_form': medical_history_form,
                           'medication_form': medication_form,
                           })
        # if user adds tag
        elif request.POST['submission_type'] == 'tag' and request.POST['tag_choice']:
            # Create a new tag relationship for this case study.
            tag = Tag.objects.get(pk=int(request.POST['tag_choice']))  # get tag object for tag_choice
            TagRelationships.objects.get_or_create(tag=tag,
                                                   case_study=case_study)  # get or create new tag relationship in the database

            case_study_tag_form = CaseStudyTagForm(request.POST)
            print(case_study_form.is_valid())
            return render(request, 'create_new_case.html',
                          {'case_study_form': case_study_form,
                           'tags': relevant_tags,
                           'medical_historys': medical_historys,
                           'medications': medications,
                           # 'case_study_question_form': case_study_question_form,
                           'case_study_tag_form': case_study_tag_form,
                           'medical_history_form': medical_history_form,
                           'medication_form': medication_form,
                           })

        elif request.POST['submission_type'] == 'save':
            if case_study_form.is_valid():
                case_study_form.save()
                return render(request, 'create_new_case.html',
                              {'case_study_form': case_study_form,
                               'tags': relevant_tags,
                               'medical_historys': medical_historys,
                               'medications': medications,
                               # 'case_study_question_form': case_study_question_form,
                               'case_study_tag_form': case_study_tag_form,
                               'medical_history_form': medical_history_form,
                               'medication_form': medication_form,
                               })
        else:
            case_study.date_submitted = timezone.now()
            case_study.save()
            case_study_form = CaseStudyForm(request.POST, instance=case_study)
            if case_study_form.is_valid():
                case_study_form.save()
                return render(request, 'create_new_case.html',
                              {'case_study_form': case_study_form,
                               'tags': relevant_tags,
                               'medical_historys': medical_historys,
                               'medications': medications,
                               # 'case_study_question_form': case_study_question_form,
                               'case_study_tag_form': case_study_tag_form,
                               'medical_history_form': medical_history_form,
                               'medication_form': medication_form,
                               })
    else:
        case_study_form = CaseStudyForm(instance=case_study)
        # case_study_question_form = CaseStudyQuestionForm()
        case_study_tag_form = CaseStudyTagForm()
        medical_history_form = MedicalHistoryForm()
        medication_form = MedicationForm()
        # case_tag_form = CaseTagForm()
    return render(request, 'create_new_case.html',
                  {'case_study_form': case_study_form,
                   'tags': relevant_tags,
                   'medical_historys': medical_historys,
                   'medications': medications,
                   # 'case_study_question_form': case_study_question_form,
                   'case_study_tag_form': case_study_tag_form,
                   'medical_history_form': medical_history_form,
                   'medication_form': medication_form,
                   })

    # return HttpResponse("Hello, world. yo!")
