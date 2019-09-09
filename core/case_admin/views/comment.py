from accounts.models import User
from core.decorators import staff_required
from django.shortcuts import render

from .common import populate_data

schema_comment = {
    "endpoint": "/caseadmin/comments/",
    "fields": [],
}


@staff_required
def view_admin_comment(request):
    data = populate_data(schema_comment, User)
    c = {
        "title": "Comment Admin",
        "model_name": "Comment",
        "data": data,
        "schema": schema_comment,
    }
    return render(request, "case-admin.html", c)
