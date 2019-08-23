from django.urls import path, re_path

from . import views

app_name = "case_admin"

urlpatterns = [
    path("users/", views.view_admin_user, name='users'),
    path("cases/", views.view_admin_case, name='cases'),
    #path("comments/", views.view_admin_commment, name='comments'),
    path("tags/", views.view_admin_tag, name='tag'),
    path("", views.view_default, name='default'),
]
