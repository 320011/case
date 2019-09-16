from django.urls import path

from . import views

app_name = "cases"

urlpatterns = [
    path("start-new-case/", views.start_new_case, name="start-new-case"),
    path("create-new-case/<int:case_study_id>", views.create_new_case, name="create-new-case"),
    path("view/<int:case_study_id>/", views.view_case, name="view-case"),
    path("api/v1/validate_answer/<int:case_study_id>/", views.validate_answer, name="validate-answer"),
    path("api/v1/submit_comment/<int:case_study_id>/", views.submit_comment, name="submit-comment"),
]
