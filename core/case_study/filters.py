import django_filters
from .models import CaseStudy

class CaseStudyFilter(django_filters.FilterSet):


	class Meta:
		model = CaseStudy
		fields = ("age_type",'date_created',)