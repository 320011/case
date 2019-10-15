from django import forms
from case_study.models import *

class TagForm(forms.Form):
    field = forms.ModelChoiceField(queryset=Tag.objects.filter(tagrelationship__isnull=False).distinct().order_by('name'))

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        for fname, f in self.fields.items():
            f.widget.attrs["class"] = "form-control"
