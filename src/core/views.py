import os
import json
import logging
# import datetime
from datetime import date
from django.views.generic import TemplateView
from django.conf import settings
from core import get_client_ip
# from django.utils.translation import ugettext as _
from django.http import (
    # HttpResponseNotFound,
    HttpResponseRedirect,
    HttpResponse
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.cache import cache
from subprocess import call, Popen, PIPE
# from rest_framework.views import APIView
from django.contrib.auth import logout
# from django.core.urlresolvers import reverse
from core import reverse
from .models import SiteUpdate
from .forms import Login as LoginForm
from django.contrib.auth import login
from . import now
from .menu import Menu
from braces import views
from django.utils.decorators import method_decorator
from lazysignup.decorators import allow_lazy_user
# from django.utils.timezone import now

log = logging.getLogger(__name__)


class EnsureCsrfCookieMixin(object):
    """
    Ensures that the CSRF cookie will be passed to the client.
    NOTE:
        This should be the left-most mixin of a view.
    """
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(EnsureCsrfCookieMixin, self).dispatch(*args, **kwargs)


# class Base(EnsureCsrfCookieMixin, TemplateView):
@method_decorator(allow_lazy_user, name='dispatch')
class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        c = super(BaseView, self).get_context_data(**kwargs)
        c["domain"] = settings.DOMAIN
        c["host"] = self.request.host

        nodir = not os.path.isdir(settings.FILES_ROOT)
        nofiles = len(os.listdir(settings.FILES_ROOT)) < 4
        c['FIRST_RUN'] = nodir or nofiles

        # c['utcnow'] = datetime.datetime.utcnow()
        # c['now'] = datetime.datetime.now()
        c['utcnow'] = now()
        c['now'] = now()

        c['year'] = date.today().year
        c['user'] = self.request.user
        if c['user'].is_lazy and not c['user'].browser_on_creation:
            c['user'].browser_on_creation = self.request.META.get('HTTP_USER_AGENT', None)
            c['user'].save()
        c['DEBUG'] = settings.DEBUG
        c['DOMAIN'] = settings.DOMAIN
        c['RAVEN_PUBLIC'] = settings.RAVEN_PUBLIC
        # c['INSTALLED_APPS'] = settings.INSTALLED_APPS

        # libraries
        c["jquery"] = True
        c["corecss"] = True
        c["chartjs"] = False
        c["nouislider"] = False
        c["dropzone"] = c['user'].is_superuser
        c['lng'] = 'en' if self.request.LANGUAGE_CODE in ('en', 'en-us')\
                   else 'ru'

        c['menu'] = Menu([])

        try:
            c['o'] = settings.OPTIONS
        except:
            c['o'] = {}
        c['ip'] = get_client_ip(self.request)
        c["analytics"] = not (
            c['user'].is_superuser or
            c['ip'].startswith('10.')
        )
        c["analytics"] = True  # just always if not DEBUG
        c['status'] = 200
        # c['mobile'] = is_mobile(self.request)
        return c

    def get(self, request, **kwargs):
        c = self.get_context_data(**kwargs)

        # Redirects
        redirect = c.get("redirect", None)
        if redirect:
            return HttpResponseRedirect(redirect)

        return self.render_to_response(c, status=c['status'])


class TreeEdit(BaseView):
    template_name = "cms_tree_edit.jinja"

    def get_context_data(self, **kwargs):
        c = super(TreeEdit, self).get_context_data(**kwargs)
        # c['article'] = Article.objects.get(pk=self.kwargs['id'])
        # c['ckeditor'] = True
        from cms.edu.models import Category
        c['roots'] = Category.objects.all()
        return c


class Celery(views.LoginRequiredMixin,
             views.SuperuserRequiredMixin,
             BaseView):
    template_name = "core_celery.jinja"
    # only_superuser = True

    def get_context_data(self, **kwargs):
        c = super(Celery, self).get_context_data(**kwargs)
        from celery.task.control import inspect
        from itertools import chain
        import psutil
        running = cache.get('celery_is_running', False)

        c['celery_exe'] = os.path.join(settings.VEBIN, 'celery')
        c['plist'] = []
        for p in psutil.process_iter():
            try:
                if p.cmdline() != ['']:
                    c['plist'] += [p.cmdline()]
            except:
                pass
            try:
                if p.cmdline()[1] == c['celery_exe']:
                    running = True
                    break
            except Exception as e:
                log.debug("Error finding celery process: {}".format(
                    str(e)
                ))

        c['psutil'] = psutil

        # Default values:
        c['registered_tasks'] = []

        c['celery_is_running'] = running
        if not running:
            return c

        i = inspect()

        registered_tasks = i.registered_tasks()
        if registered_tasks is not None:
            c['registered_tasks'] = set(chain.from_iterable(
                registered_tasks.values()))
        # c['registered_tasks'] = i.registered_tasks()

        # stats = cache.get_or_set(
        #     'celery_stats',
        #     lambda: inspect().stats(),
        #     100
        # )
        return c

    def post(self, request, **kwargs):
        c = self.get_context_data(**kwargs)

        if not c['user'].is_superuser:
            return HttpResponse('{}')
        res = {}

        # Is Supervisor installed?
        if not os.path.isdir('/etc/supervisor/conf.d'):
            # TODO: install supervisor
            try:
                call(['sudo', 'apt-get', 'install', 'supervisor'])
            except Exception as e:
                if not os.path.isdir('/etc/supervisor/conf.d'):
                    log.debug('Installing Supervisor failed with: {}'.format(
                        str(e)
                    ))
                    # raise ValueError("still no Supervisor")
                res['no_supervisor'] = True

        # Celery Supervisor config file
        sv_config = '/etc/supervisor/conf.d/celery-{}.conf'.format(
            settings.DOMAIN
        )
        if not os.path.isfile(sv_config):
            res['no_supervisor_config'] = True
            # TODO: create sv config file
        else:
            import configparser
            config = configparser.ConfigParser()
            # config.sections()
            config.read(sv_config)
            # config.sections()
            # res['sections'] = config.sections()

            # Supervisor config params for Celery
            if "program:celery" in config:
                params = config["program:celery"]
                res['params'] = dict(params)
        return HttpResponse(json.dumps(res))


# Travis payload format:
# https://docs.travis-ci.com/user/notifications#Webhooks-Delivery-Format
class Updates(views.LoginRequiredMixin,
              views.SuperuserRequiredMixin,
              BaseView):
    template_name = "core_updates.jinja"
    # only_superuser = True

    def get_context_data(self, **kwargs):
        c = super(Updates, self).get_context_data(**kwargs)
        c["timeago"] = True
        c["updates"] = SiteUpdate.objects.filter(commit_message__isnull=False,
                                                 started__isnull=False) \
                                         .order_by('-started')
        return c


class Nginx(views.LoginRequiredMixin,
            views.SuperuserRequiredMixin,
            BaseView):
    template_name = "core_nginx.jinja"
    # only_superuser = True

    def get_context_data(self, **kwargs):
        c = super(Nginx, self).get_context_data(**kwargs)
        try:
            p = Popen(['nginx', '-V'])
            nginxv, err = p.communicate(stdout=PIPE)
        except:
            nginxv = '''nginx version: nginx/1.10.0 (Ubuntu)...'''

        c["nginxv"] = nginxv
        c["arguments"] = nginxv
        return c


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class Login(EnsureCsrfCookieMixin, BaseView):
    template_name = "core_login.jinja"

    def get_context_data(self, **kwargs):
        c = super(Login, self).get_context_data(**kwargs)
        c['menu'] = {}
        # c['form'] = LoginForm
        return c

    def get(self, request, **kwargs):
        c = self.get_context_data(**kwargs)
        if request.user.is_authenticated and not request.user.is_lazy:
            return HttpResponseRedirect(reverse("index", host=c['host'].name))
        else:
            return self.render_to_response(c, status=c['status'])

    def post(self, request, **kwargs):
        f = LoginForm(request.POST)
        # request.GET.get('redirect')
        # Check form input data (email and password)
        if f.is_valid():
            login(request, f.cleaned_data['user'])
            return HttpResponse(
                json.dumps({'code': 0}),
                content_type='application/json'
            )
        else:
            return HttpResponse(
                json.dumps({'errors': f.errors}),
                content_type='application/json'
            )


# class Logout(APIView):
class Logout(EnsureCsrfCookieMixin, BaseView):
    def get(self, request, **kwargs):
        c = self.get_context_data(**kwargs)
        logout(request)
        return HttpResponseRedirect(reverse("index", host=c['host'].name))

    def post(self, request, **kwargs):
        logout(request)
        return HttpResponse("{}", content_type='application/json')
