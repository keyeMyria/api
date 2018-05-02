import os
import sys
import datetime
# import distutils
from django.utils.timezone import utc
from django.contrib import sitemaps
from rest_framework.pagination import CursorPagination as CP
import logging
log = logging.getLogger(__name__)

try:
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
except Exception:
    log.error('install pymorphy2')


class CursorPagination(CP):
    ordering = 'pk'
    # ordering = '-created'
    # ordering = 'date_joined'
    # ordering = '-date_joined'


try:
    from django_hosts.resolvers import reverse as reverse_hosts
    reverse = reverse_hosts
    # from django.core.urlresolvers import reverse as reverse_django
    # reverse = reverse_django
except Exception:
    log.error('install django_hosts')


default_app_config = 'core.apps.CoreConfig'


def get_git_root(path=None):
    if path is None:
        path = os.getcwd()
    try:
        import git
    except Exception:
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


class Sitemap(sitemaps.Sitemap):
    def _urls(self, page, protocol, domain):
        urls = []
        latest_lastmod = None
        all_items_lastmod = True  # track if all items have a lastmod
        for item in self.paginator.page(page).object_list:
            loc = "{}:{}".format(protocol, self.__get('location', item))
            priority = self.__get('priority', item)
            lastmod = self.__get('lastmod', item)
            if all_items_lastmod:
                all_items_lastmod = lastmod is not None
                if (all_items_lastmod and
                        (latest_lastmod is None or lastmod > latest_lastmod)):
                    latest_lastmod = lastmod
            url_info = {
                'item': item,
                'location': loc,
                'lastmod': lastmod,
                'changefreq': self.__get('changefreq', item),
                'priority': str(priority if priority is not None else ''),
            }
            urls.append(url_info)
        if all_items_lastmod and latest_lastmod:
            self.latest_lastmod = latest_lastmod
        return urls


def confirm(question, default="y"):
    """Ask a yes/no question via input() and return answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    # distutils.util.strtobool(val)
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default in ('yes', 'y'):
        prompt = " [Y/n] "
    elif default in ('no', 'n'):
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


# Detecting mobile device
# Taken from here: http://detectmobilebrowsers.com/
# removed for pep8
