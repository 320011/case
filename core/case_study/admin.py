from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(CaseStudy)
admin.site.register(Playlist)
admin.site.register(TagRelationship)
admin.site.register(MedicalHistory)
admin.site.register(Medication)
admin.site.register(Attempt)
admin.site.register(Comment)
admin.site.register(Other)
admin.site.register(CommentReport)
