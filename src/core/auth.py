from django.contrib import auth
from django.utils.functional import SimpleLazyObject

#
# Taken from the official Django Auth Middleware:
# https://github.com/django/django/blob/master/django/contrib/auth/middleware.py
#


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    # if isinstance(request._cached_user,
    #               django.contrib.auth.models.AnonymousUser):
    #     request._cached_user = User.objects.get(pk=1)
    return request._cached_user


class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        request.user = SimpleLazyObject(lambda: get_user(request))
