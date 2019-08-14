from django.contrib import admin
from .models import Question, Tag, CaseStudy, MedicalHistory, Medication

# Register your models here.
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(CaseStudy)
admin.site.register(MedicalHistory)
admin.site.register(Medication)