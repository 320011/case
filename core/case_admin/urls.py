from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^/api/v1/user/$', views.view_admin_user, name='user'),
    re_path(r'^/api/v1/case/$', views.view_admin_case, name='case'),
    re_path(r'^/api/v1/comment/$', views.view_admin_commment, name='comment'),
    re_path(r'^/api/v1/tag/$', views.view_admin_tag, name='tag'),
    
]
