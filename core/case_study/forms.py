from django import forms
from django.forms import ModelForm

from .models import Tag, CaseStudy, MedicalHistory, Medication


# populate patient particulars and description
class CaseStudyForm(ModelForm):
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
            "answer_1",
            "answer_2",
            "answer_3",
            "answer_4",
            "is_submitted"
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "answer_1": forms.Textarea(attrs={"rows": 4}),
            "answer_2": forms.Textarea(attrs={"rows": 4}),
            "answer_3": forms.Textarea(attrs={"rows": 4}),
            "answer_4": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super(CaseStudyForm, self).__init__(*args, **kwargs)
        for fname, f in self.fields.items():
            f.widget.attrs["class"] = "form-control"

    def clean(self):
        is_submitted = self.cleaned_data.get("is_submitted")
        if is_submitted:
            age = self.cleaned_data.get("age")
            description = self.cleaned_data.get("description")
            height = self.cleaned_data.get("height")
            weight = self.cleaned_data.get("weight")
            scr = self.cleaned_data.get("scr")
            age_type = self.cleaned_data.get("age_type")
            sex = self.cleaned_data.get("sex")
            question = self.cleaned_data.get("question")
            answer_1 = self.cleaned_data.get("answer_1")
            answer_2 = self.cleaned_data.get("answer_2")
            answer_3 = self.cleaned_data.get("answer_3")
            answer_4 = self.cleaned_data.get("answer_4")
            if not age or \
                    not description or \
                    not height or \
                    not weight or \
                    not scr or \
                    not age_type or \
                    not sex or \
                    not question or \
                    not answer_1 or \
                    not answer_2 or \
                    not answer_3 or \
                    not answer_4:
                errordict = {}
                for item in self.cleaned_data:
                    if not self.cleaned_data[item]:
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
