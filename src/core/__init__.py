import os
import sys
import functools
import re
import datetime
from django.utils.timezone import utc
from django.core.validators import URLValidator

default_app_config = 'core.apps.CoreConfig'


def now():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


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


def apps():
    """Iterate all apps (read file-system)"""
    src = os.path.dirname(os.path.dirname(__file__))
    for app in os.listdir(src):
        path = os.path.join(src, app)
        if not os.path.isdir(path):
            continue
        if not os.path.isfile(os.path.join(path, '__init__.py')):
            continue
        yield (app, path)


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


# Detecting mobile device
# Taken from here: http://detectmobilebrowsers.com/
# removed for pep8
