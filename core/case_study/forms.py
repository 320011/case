from django import forms
from django.forms import ModelForm

from .models import Tag, CaseStudy, MedicalHistory, Medication


# populate patient particulars and description
class CaseStudyForm(ModelForm):
    confirm_patient_anonymous = forms.BooleanField(required=False)
    class Meta:
        model = CaseStudy
        fields = [
            "height",
            "weight",
            "scr",
            "age_type",
            "age",
            "sex",
            "description",
            "question",
            "answer_a",
            "answer_b",
            "answer_c",
            "answer_d",
            "answer",
            "feedback",
            "is_submitted",
            "is_anonymous",
            "confirm_patient_anonymous"
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "answer_a": forms.Textarea(attrs={"rows": 4}),
            "answer_b": forms.Textarea(attrs={"rows": 4}),
            "answer_c": forms.Textarea(attrs={"rows": 4}),
            "answer_d": forms.Textarea(attrs={"rows": 4}),
            "feedback": forms.Textarea(attrs={"rows": 4})
        }

    def __init__(self, *args, **kwargs):
        super(CaseStudyForm, self).__init__(*args, **kwargs)
        for fname, f in self.fields.items():
            if fname == 'is_anonymous' or fname == 'confirm_patient_anonymous':
                f.widget.attrs["class"] = "form-check-input"
            else:
                f.widget.attrs["class"] = "form-control"

    def clean(self):
        is_submitted = self.cleaned_data.get("is_submitted")
        if is_submitted:
            age = self.cleaned_data.get("age")
            description = self.cleaned_data.get("description")
            age_type = self.cleaned_data.get("age_type")
            sex = self.cleaned_data.get("sex")
            question = self.cleaned_data.get("question")
            answer_a = self.cleaned_data.get("answer_a")
            answer_b = self.cleaned_data.get("answer_b")
            answer_c = self.cleaned_data.get("answer_c")
            answer_d = self.cleaned_data.get("answer_d")
            answer = self.cleaned_data.get("answer")
            feedback = self.cleaned_data.get("feedback")
            confirm_patient_anonymous = self.cleaned_data.get('confirm_patient_anonymous')
            check_fields = ["age", "description", "age_type", "sex", "question", "answer_a", "answer_b", "answer_c", "answer_d", "answer", "feedback", "confirm_patient_anonymous"]
            if not age or \
                    not description or \
                    not age_type or \
                    not sex or \
                    not question or \
                    not answer_a or \
                    not answer_b or \
                    not answer_c or \
                    not answer_d or \
                    not answer or \
                    not feedback or \
                    not confirm_patient_anonymous:
                errordict = {}
                for item in check_fields:
                    if not self.cleaned_data[item]:
                        if item == "confirm_patient_anonymous":
                            errordict[item] = "Please confirm that you have not revealed any identifying information for the case study patient."
                        else:
                            errordict[item] = "This is not a valid " + str(item).replace("_", " ")
                raise forms.ValidationError(errordict)


class TagModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CaseStudyTagForm(forms.Form):
    tag_choice = TagModelChoiceField(queryset=Tag.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(CaseStudyTagForm, self).__init__(*args, **kwargs)
        for fname, f in self.fields.items():
            f.widget.attrs["class"] = "form-control"


# populate patient medical history
class MedicalHistoryForm(ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 1}),
        }

    def __init__(self, *args, **kwargs):
        super(MedicalHistoryForm, self).__init__(*args, **kwargs)
        for fname, f in self.fields.items():
            f.widget.attrs["class"] = "form-control"


# populate patient medication
class MedicationForm(ModelForm):
    class Meta:
        model = Medication
        fields = ["name"]
        widgets = {
            "name": forms.Textarea(attrs={"rows": 1}),
        }

    def __init__(self, *args, **kwargs):
        super(MedicationForm, self).__init__(*args, **kwargs)
        for fname, f in self.fields.items():
            f.widget.attrs["class"] = "form-control"

