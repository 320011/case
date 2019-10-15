from django.urls import path

from case_study.views import case_search, create_case, view_case

app_name = "cases"

urlpatterns = [
    path("new/", create_case.start_new_case, name="start-new-case"),
    path("edit/<int:case_study_id>", create_case.create_new_case, name="create-new-case"),
    path("view/<int:case_study_id>/", view_case.view_case, name="view-case"),
    path("search/", case_search.search, name="search"),
    path("search/advanced/", case_search.advsearch, name="advsearch"),
    path("drafts/", create_case.unsubmitted_cases, name="unsubmitted-cases"),
    path("api/v1/validate_answer/<int:case_study_id>/", view_case.validate_answer, name="validate-answer"),
    path("api/v1/submit_comment/<int:case_study_id>/", view_case.submit_comment, name="submit-comment"),
    path("api/v1/delete_unsubmitted_case/", create_case.delete_unsubmitted_case, name="delete-unsubmitted-case"),
    path("api/v1/submit_report/<int:report_id>", view_case.submit_report, name="submit-report"),
    path("api/v1/delete_comment/<int:comment_id>/", view_case.delete_comment, name="delete_comment"),
]