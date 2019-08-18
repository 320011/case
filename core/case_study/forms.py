from django.forms import ModelForm
from .models import Question, CaseStudy, MedicalHistory, Medication #,TagRelationships


# populate patient particulars and description
class CaseStudyForm(ModelForm):
    class Meta:
        model = CaseStudy
        fields = ['height', 'weight', 'scr', 'age_type', 'age', 'sex','description', 'answer_1', 'answer_2', 'answer_3', 'answer_4']

# select existing question
class CaseStudyQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['body']

# populate patient medical history
class MedicalHistoryForm(ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['body']

# populate patient medication
class MedicationForm(ModelForm):
    class Meta:
        model = Medication
        fields = ['name']

# # select tags for case study
# class CaseTagForm(ModelForm):
#     class Meta: 
#         model = TagRelationships
#         fields = ['tag']