import os
import sys
import functools
from django.core.validators import URLValidator

default_app_config = 'core.apps.CoreConfig'


def underDjangoDebugServer():
    if len(sys.argv) > 1:
        return sys.argv[1] in (
            'runserver',
            'runcserver',
            'runserver_plus') or \
            sys.argv[1] == 'runworker' and len(sys.argv) > 2 and \
            sys.argv[2] == '-v2'  # channels
    else:
        return False


def correctURL(url):
    val = URLValidator()
    try:
        val(url)
        return True
    except:
        return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def travis(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = None
        if os.getenv('CI', '') == 'true':
            res = func(*args, **kwargs)
        return res
    return wrapper
