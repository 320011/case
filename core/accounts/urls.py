from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = "users"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="auth-login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("profile/", views.view_profile, name="profile"),
    path("profile/results", views.view_profile_results, name="profile_results"),
    path("signup/", views.view_signup, name="signup"),
    path("activate/", views.view_activate, name="activate"),
    
   
    path('password_change', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change_done', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'), name='password_change_done'),

    path('password_reset',auth_views.PasswordResetView.as_view(template_name='reset.html'),name='password_reset'),

    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    
    path('password_reset_confirm', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_complete'),
    
    path('password_reset_complete', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),

]
