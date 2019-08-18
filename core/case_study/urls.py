from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='cases'),
    path('start-new-case/', views.start_new_case, name='start-new-case'),
    path('create-new-case/<int:case_study_id>', views.create_new_case, name='create-new-case'),
]