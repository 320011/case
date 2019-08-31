from accounts.models import User
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied


def staff_required(function):
    def wrapper(request, *args, **kw):
        if not request.user.is_staff:
            raise PermissionDenied()
        else:
            return function(request, *args, **kw)
    return wrapper
