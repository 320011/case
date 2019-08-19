from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'users'

urlpatterns = [
    path('<int:user_id>', views.profile, name='profile'),
    path('<int:user_id>/results', views.profile_results, name='profile_results'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/',  login_required(views.UserView.as_view()), name='profile'),
    path('signup/', views.signup, name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
   
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
