import django_filters
from .models import CaseStudy

class CaseStudyFilter(django_filters.FilterSet):

	CHOICES = (
		('ascending','Ascending'),
		('descending', 'Descending'))

	ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')

	class Meta:
		model = CaseStudy
		fields = ("description",)

	def filter_by_order(self, queryset, name, value):
		expression = 'created' if value == 'ascending' else '-created'
		return queryset.order_by(expression)