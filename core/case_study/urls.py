from django.urls import path

from . import views

app_name = "cases"

urlpatterns = [
    path("start-new-case/", views.start_new_case, name="start-new-case"),
    path("create-new-case/<int:case_study_id>", views.create_new_case, name="create-new-case"),
    path("view/<int:case_study_id>/", views.view_case, name="view-case"),
    path("api/v1/validate_answer/<int:case_study_id>/", views.validate_answer, name="validate-answer"),
    path("api/v1/submit_comment/<int:case_study_id>/", views.submit_comment, name="submit-comment"),
    # path("api/v1/add_medical_history/<int:case_study_id>/", views.add_medical_history, name="add-medical-history"),
    # path("api/v1/add_medication/<int:case_study_id>/", views.add_medication, name="add-medication"),
    # path("api/v1/add_other/<int:case_study_id>/", views.add_other, name="add-other"),
    # path("api/v1/add_tag/<int:case_study_id>/", views.add_tag, name="add-tag"),
]
