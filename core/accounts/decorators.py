from django.http import HttpResponseRedirect


def anon_required(func):
    def _anon_required(*args, **kwargs):
        if args[0].user.is_authenticated:
            return HttpResponseRedirect("/user/logout")
        return func(*args, **kwargs)

    return _anon_required
