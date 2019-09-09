import copy
import json
from datetime import datetime

import openpyxl
from accounts.models import User
from core.decorators import staff_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sessions.models import Session
from django.core.exceptions import FieldDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from ..forms import TagImportForm

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
