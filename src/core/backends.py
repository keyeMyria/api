import django
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from .models import User
from django.core.exceptions import ValidationError


def is_valid_email(email):
    try:
        django.core.validators.validate_email(email)
        return True
    except ValidationError:
        return False
    return False


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        """This function checks (username, password) pair at login"""
        if is_valid_email(username):
            try:
                user = User.objects.get(email__iexact=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        """Try to get a user
        If failed - return an anonymous user (return None)"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = User
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
            return self._user_class
