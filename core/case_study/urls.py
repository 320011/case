from django.urls import path

from . import views

app_name = "cases"

urlpatterns = [
    path("new/", views.start_new_case, name="start-new-case"),
    path("edit/<int:case_study_id>", views.create_new_case, name="create-new-case"),
    path("view/<int:case_study_id>/", views.view_case, name="view-case"),
    path("search/", views.search, name="search"),
    path("search/advanced/", views.advsearch, name="advsearch"),
    path("drafts/", views.unsubmitted_cases, name="unsubmitted-cases"),
    path("api/v1/validate_answer/<int:case_study_id>/", views.validate_answer, name="validate-answer"),
    path("api/v1/submit_comment/<int:case_study_id>/", views.submit_comment, name="submit-comment"),
    path("api/v1/delete_unsubmitted_case/", views.delete_unsubmitted_case, name="delete-unsubmitted-case"),
]
