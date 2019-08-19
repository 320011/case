# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from .forms import CaseStudyForm, CaseStudyTagForm, MedicalHistoryForm, MedicationForm  # , CaseTagForm
from .models import Tag, TagRelationships, CaseStudy


def index(request):
    return HttpResponse("Hello, world. You're at the case study index.")


def start_new_case(request):
    case = CaseStudy.objects.create(created_by=request.user)
    return HttpResponseRedirect(
        reverse('cases:create-new-case', kwargs={'case_study_id': case.id}))


def create_new_case(request, case_study_id):
    case_study, created = CaseStudy.objects.get_or_create(pk=case_study_id)
    relevant_tags = TagRelationships.objects.filter(case_study=case_study)
    if request.method == 'POST':
        case_study_form = CaseStudyForm(request.POST, instance=case_study)
        # case_study_question_form = CaseStudyQuestionForm(request.POST)
        case_study_tag_form = CaseStudyTagForm(request.POST)
        medical_history_form = MedicalHistoryForm(request.POST)
        medication_form = MedicationForm(request.POST)

        if request.POST['submission_type'] == 'tag' and request.POST['tag_choice']:
            # Create a new tag for this case study.
            tag = Tag.objects.get(pk=int(request.POST['tag_choice']))
            TagRelationships.objects.get_or_create(tag=tag, case_study=case_study)

            case_study_tag_form = CaseStudyTagForm(request.POST)
            print(case_study_form.is_valid())
            return render(request, 'create_new_case.html',
                          {'case_study_form': case_study_form,
                           'tags': relevant_tags,
                           # 'case_study_question_form': case_study_question_form,
                           'case_study_tag_form': case_study_tag_form,
                           'medical_history_form': medical_history_form,
                           'medication_form': medication_form,
                           })
        else:
            print(request.POST)
            print(case_study_form.is_valid())
            case_study_form.save()
            if case_study_form.is_valid() and case_study_tag_form.is_valid():
                case_study_form.save()
                return render(request, 'create_new_case.html',
                      {'case_study_form': case_study_form,
                       'tags': relevant_tags,
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
                   # 'case_study_question_form': case_study_question_form,
                   'case_study_tag_form': case_study_tag_form,
                   'medical_history_form': medical_history_form,
                   'medication_form': medication_form,
                   })  # , 'case_tag_form':case_tag_form})



    # return HttpResponse("Hello, world. yo!")
