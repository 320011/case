from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'users'

urlpatterns = [
	path('', views.home, name='accounts-home'),
	path('register',views.register, name='accounts-register'),
    path('<int:user_id>', views.profile, name='profile'),
    path('<int:user_id>/results', views.profile_results, name='profile_results'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/user/login'), name='logout'),
    path('profile/',  login_required(views.UserView.as_view()), name='profile'),
    path('signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]