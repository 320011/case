from django.urls import path

from . import views

app_name = "case_admin"

urlpatterns = [
    path("users/", views.view_admin_user, name='users'),
    path("users/<int:user_id>", views.api_admin_user, name='api_users'),
    path("cases/", views.view_admin_case, name='cases'),
    path("cases/<int:case_id>", views.api_admin_case, name='api_cases'),
    #path("comments/", views.view_admin_commment, name='comments'),
    path("tags/", views.view_admin_tag, name='tags'),
    path("tags/import", views.api_admin_tag_import, name='tag_import'),
    path("tags/<int:tag_id>", views.api_admin_tag, name='tags'),
    path("", views.view_default, name='default'),
]
