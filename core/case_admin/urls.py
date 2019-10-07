from django.urls import path

from case_admin.views import common, case, comment, tag, user, question

app_name = "case_admin"

urlpatterns = [
    path("users/", user.view_admin_user, name='users'),
    path("users/review", user.view_admin_user_review, name='users_review'),
    path("users/<int:user_id>", user.api_admin_user, name='api_users'),
    path("cases/", case.view_admin_case, name='cases'),
    path("cases/review", case.view_admin_case_review, name='cases_review'),
    path("cases/<int:case_id>", case.api_admin_case, name='api_cases'),
    path("questions/", question.view_admin_question, name='questions'),
    path("questions/import", question.api_admin_question_import, name='tquestion_import'),
    path("questions/<int:question_id>", question.api_admin_question, name='api_questions'),
    path("tags/", tag.view_admin_tag, name='tags'),
    path("tags/import", tag.api_admin_tag_import, name='tag_import'),
    path("tags/<int:tag_id>", tag.api_admin_tag, name='api_tags'),
    path("comments/", comment.view_admin_comment, name='comments'),
    path("comments/review", comment.view_admin_comment_review, name='comments_review'),
    path("comments/<int:comment_id>", comment.api_admin_comment, name='api_comments'),
    path("", common.view_landing, name='default'),
]
