import os
import sys
import datetime
import pymorphy2
from django.utils.timezone import utc

from django_hosts.resolvers import reverse as reverse_hosts
reverse = reverse_hosts
# from django.core.urlresolvers import reverse as reverse_django
# reverse = reverse_django

morph = pymorphy2.MorphAnalyzer()

default_app_config = 'core.apps.CoreConfig'


def get_git_root(path):
    try:
        import git
    except:
        import pip
        pip.main(['install', '--user', 'gitpython'])
        import git

    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root


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
