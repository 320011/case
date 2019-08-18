from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='cases'),
    path('create-new-case/', views.create_new_case, name='create-new-case'),
]