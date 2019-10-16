from django.urls import path

from . import views

app_name = "analytics"

urlpatterns = [
    path("", views.view_landing, name='default'),
    path("question", views.view_question, name='question'),
    path("tag", views.view_tag, name='tag'),
    path("medicalhistory", views.view_medicalhistory, name='medicalhistory'),
    path("comment", views.view_comment, name='comment'),
    path("casestudy", views.view_casestudy, name='casestudy'),
    path("medication", views.view_medication, name='medication'),
    path("tagrelationship", views.view_tagrelationship, name='tagrelationship'),
    path("other", views.view_other, name='other'),
    path("commentreport", views.view_commentreport, name='commentreport'),
    path("attempt", views.view_attempt, name='attempt'),
    path("user", views.view_user, name='user'),
    path("api/v1/tag_performance", views.tag_performance, name='tag_performance'),
]
