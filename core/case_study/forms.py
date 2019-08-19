from django.forms import ModelForm
from django import forms
from .models import Question, Tag, CaseStudy, MedicalHistory, Medication #,TagRelationships

# populate patient particulars and description
class CaseStudyForm(ModelForm):
    class Meta:
        model = CaseStudy
        fields = ['height', 'weight', 'scr', 'age_type', 'age', 'sex','description', 'question', 'answer_1', 'answer_2', 'answer_3', 'answer_4']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'answer_1': forms.Textarea(attrs={'rows': 4}),
            'answer_2': forms.Textarea(attrs={'rows': 4}),
            'answer_3': forms.Textarea(attrs={'rows': 4}),
            'answer_4': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(CaseStudyForm, self).__init__(*args, **kwargs)

        # you can iterate all fields here
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control'

# custom ModelChoiceForm for Question 
# class QuestionModelChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#          return obj.body

# select existing question
# class CaseStudyQuestionForm(ModelForm):
#     question_choice = QuestionModelChoiceField(queryset = Question.objects.all())
#     class Meta:
#         model = Question
#         fields = ['body']
#
#     def __init__(self, *args, **kwargs):
#         super(CaseStudyQuestionForm, self).__init__(*args, **kwargs)
#
#         # you can iterate all fields here
#         for fname, f in self.fields.items():
#             f.widget.attrs['class'] = 'form-control'
    
    # def save(self, commit=True):
    #     case_study, created = CaseStudy.objects.update_or_create(user=self.user, author=self.author, defaults={'is_follow': self.cleaned_data.get('is_follow'), 'review': self.cleaned_data.get('review')} )
    #     #rest of your logic
    #     return case_study

class TagModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

class CaseStudyTagForm(forms.Form):
    tag_choice = TagModelChoiceField(queryset=Tag.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(CaseStudyTagForm, self).__init__(*args, **kwargs)

        # you can iterate all fields here
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control'

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