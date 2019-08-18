from django.urls import path

from . import views

urlpatterns = [
	path('', views.home, name='accounts-home'),
	path('register',views.register, name='accounts-register'),
    path('<int:user_id>', views.profile, name='profile'),
    path('<int:user_id>/results', views.profile_results, name='profile_results'),
]