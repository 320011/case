from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.view_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("profile/", views.view_profile, name="profile"),
    path("profile/results", views.view_profile_results, name="profile_results"),
    path("signup/", views.view_signup, name="signup"),
    path("activate/", views.view_activate, name="activate"),
    path("profile/settings", views.view_settings, name="profile_settings")
]
