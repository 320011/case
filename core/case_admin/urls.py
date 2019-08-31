from django.urls import path

from . import views

app_name = "case_admin"

urlpatterns = [
    path("users/", views.view_admin_user, name='users'),
    path("users/<int:user_id>", views.api_admin_user, name='api_users'),
    path("cases/", views.view_admin_case, name='cases'),
    #path("comments/", views.view_admin_commment, name='comments'),
    path("tags/", views.view_admin_tag, name='tag'),
    path("", views.view_default, name='default'),
]
