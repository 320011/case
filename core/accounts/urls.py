from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.view_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("profile/", views.view_profile, name="profile"),
    path("signup/", views.view_signup, name="signup"),
    path("activate/", views.view_activate, name="activate"),
    path("settings", views.view_settings, name="profile_settings"),
    path("settings/password", views.view_change_password, name="change_password"),
    path("settings/delete", views.view_delete_account, name="delete_account"),
    path("settings/delete/confirm", views.api_delete_account_confirm, name="delete_account_confirm"),
]
