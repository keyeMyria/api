import os
import json
import logging
# import datetime
from datetime import date
from django.views.generic import TemplateView
from django.conf import settings
from core import get_client_ip
from rest_framework import viewsets
# from django.utils.translation import ugettext as _
from django.http import (
    # HttpResponseNotFound,
    HttpResponseRedirect,
    HttpResponse,
    JsonResponse
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.cache import cache
from subprocess import call, Popen, PIPE
# from rest_framework.views import APIView
from django.contrib.auth import logout
# from django.core.urlresolvers import reverse
from core import reverse
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SiteUpdate, LoginAttempt
from .forms import Login as LoginForm
from django.contrib.auth import login
from . import now
from .menu import Menu
from braces import views
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from raven.contrib.django.raven_compat.models import client
from django.contrib.auth import get_user_model
User = get_user_model()
# from lazysignup.decorators import allow_lazy_user
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
        return super().dispatch(*args, **kwargs)


# @method_decorator(allow_lazy_user, name='dispatch')
class BaseView(
        # EnsureCsrfCookieMixin,
        TemplateView,
):
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c["domain"] = settings.DOMAIN

        # Added by django_hosts middleware:
        c["host"] = self.request.host
        # c["host"] = self.request.get_host().split(':')[0]

        try:
            nodir = not os.path.isdir(settings.FILES_ROOT[0])
            nofiles = nodir or len(os.listdir(settings.FILES_ROOT[0])) < 4
            c['FIRST_RUN'] = nodir or nofiles
        except Exception:
            client.captureException()

        import rparser
        c['rparser_version'] = rparser.__version__

        # c['utcnow'] = datetime.datetime.utcnow()
        # c['now'] = datetime.datetime.now()
        c['utcnow'] = now()
        c['now'] = now()
        c['CURRENTYEAR'] = date.today().year
        c['user'] = self.request.user
        c['ip'] = get_client_ip(self.request)

        if c['user'].is_authenticated:
            # if c['user'].is_lazy and not c['user'].browser_on_creation:
            #     c['user'].browser_on_creation = self.request.META.get(
            #         'HTTP_USER_AGENT', None
            #     )
            #     c['user'].save()
            try:
                # if c['user'].is_lazy and not c['user'].created_from_ip:
                if not c['user'].created_from_ip:
                    c['user'].created_from_ip = c['ip']
                    c['user'].save()
            except Exception:
                client.captureException()
        # created_from_ip

        c['DEBUG'] = settings.DEBUG
        c['DOMAIN'] = settings.DOMAIN
        c['RAVEN_PUBLIC'] = settings.RAVEN_PUBLIC

        # libraries
        c["jquery"] = True
        c["corecss"] = True
        c["chartjs"] = False
        c["nouislider"] = False
        c["dropzone"] = c['user'].is_superuser
        c['lng'] = 'en' if self.request.LANGUAGE_CODE in ('en', 'en-us')\
                   else 'ru'

        c['menu'] = Menu([])
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
        c = super().get_context_data(**kwargs)
        # c['article'] = Article.objects.get(pk=self.kwargs['id'])
        # c['ckeditor'] = True
        from cms.edu.models import Category
        c['roots'] = Category.objects.all()
        return c


class Celery(views.LoginRequiredMixin,
             views.SuperuserRequiredMixin,
             BaseView):
    template_name = "core_celery.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
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
            except Exception:
                pass
            try:
                if p.cmdline()[1] == c['celery_exe']:
                    running = True
                    break
            except Exception as e:
                # Got: list index out of range
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
            c['registered_tasks'] = sorted(list(set(chain.from_iterable(
                registered_tasks.values()))))
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
        return JsonResponse(res)


# Travis payload format:
# https://docs.travis-ci.com/user/notifications#Webhooks-Delivery-Format
class Updates(views.LoginRequiredMixin,
              views.SuperuserRequiredMixin,
              BaseView):
    template_name = "core_updates.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c["timeago"] = True
        c["updates"] = SiteUpdate.objects.filter(
            commit_message__isnull=False,
            started__isnull=False
        ).order_by('-started')
        return c


class Profile(
        views.LoginRequiredMixin,
        BaseView
):
    template_name = "core_profile.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c["timeago"] = True
        c["updates"] = SiteUpdate.objects.filter(
            commit_message__isnull=False,
            started__isnull=False
        ).order_by('-started')
        return c


class Nginx(views.LoginRequiredMixin,
            views.SuperuserRequiredMixin,
            BaseView):
    template_name = "core_nginx.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        try:
            p = Popen(['nginx', '-V'], stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            nginxv = err.decode('utf8')  # WTF? but this is in err, really
        except Exception as e:
            nginxv = str(e)

        from .tasks.geoip import versions_file
        try:
            versions = json.load(open(versions_file, 'r'))
        except Exception:
            versions = {}
            c['city_version'] = versions.get('city', '')
            c['country_version'] = versions.get('country', '')

        c['modules'] = {
            'geoip': '--with-http_geoip_module' in nginxv
        }

        c["nginxv"] = nginxv
        c["arguments"] = nginxv
        return c


class Cluster(views.LoginRequiredMixin,
              views.SuperuserRequiredMixin,
              BaseView):
    template_name = "core_cluster.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        try:
            p = Popen(['nginx', '-V'], stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            nginxv = err.decode('utf8')  # WTF? but this is in err, really
        except Exception as e:
            nginxv = str(e)

        from .tasks.geoip import versions_file
        try:
            versions = json.load(open(versions_file, 'r'))
        except Exception:
            versions = {}
            c['city_version'] = versions.get('city', '')
            c['country_version'] = versions.get('country', '')

        c['modules'] = {
            'geoip': '--with-http_geoip_module' in nginxv
        }

        c["nginxv"] = nginxv
        c["arguments"] = nginxv
        return c


class Postgres(
        views.LoginRequiredMixin,
        views.SuperuserRequiredMixin,
        BaseView
):
    template_name = "core_postgres.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['db_all'] = dbs = settings.DATABASES
        c['pg_locations'] = set()
        for db in dbs:
            c['pg_locations'].add((dbs[db]['HOST'], dbs[db]['PORT']))

        c['db_pg'] = [
            db for db in dbs
            if dbs[db]['ENGINE'] in (
                    'django.db.backends.postgresql_psycopg2',
            )]
        try:
            p = Popen(['nginx', '-V'], stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            nginxv = err.decode('utf8')  # WTF? but this is in err, really
        except Exception as e:
            nginxv = str(e)

        from .tasks.geoip import versions_file
        try:
            versions = json.load(open(versions_file, 'r'))
        except Exception:
            versions = {}
            c['city_version'] = versions.get('city', '')
            c['country_version'] = versions.get('country', '')

        c['modules'] = {
            'geoip': '--with-http_geoip_module' in nginxv
        }

        c["nginxv"] = nginxv
        c["arguments"] = nginxv
        return c


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class Login(
        # EnsureCsrfCookieMixin,
        BaseView,
):
    template_name = "core_login.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['menu'] = {}
        # c['form'] = LoginForm
        return c

    def get(self, request, **kwargs):
        c = self.get_context_data(**kwargs)
        if request.user.is_authenticated:  # and not request.user.is_lazy:
            return HttpResponseRedirect(reverse("index", host=c['host'].name))
        else:
            return self.render_to_response(c, status=c['status'])

    def post(self, request, **kwargs):
        c = self.get_context_data(**kwargs)
        f = LoginForm(request.POST)
        record = LoginAttempt(ip=c['ip'])
        if f.is_valid():
            login(request, f.cleaned_data['user'])
            record.user = f.cleaned_data['user']
            record.save()
            return JsonResponse({'code': 0})
        else:
            log.debug(f.errors)
            record.login = f.cleaned_data['username']
            record.password = f.cleaned_data['password']
            record.save()
            return JsonResponse({'errors': f.errors})


class Logout(
        # EnsureCsrfCookieMixin,
        BaseView,
):
    def get(self, request, **kwargs):
        c = self.get_context_data(**kwargs)
        logout(request)
        return HttpResponseRedirect(reverse("index", host=c['host'].name))

    def post(self, request, **kwargs):
        logout(request)
        return HttpResponse("{}", content_type='application/json')


# class StudentViewSet2(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing user instances.
#     """
#     serializer_class = StudentSerializer
#     queryset = User.objects.all()

# class UsersViewSet(viewsets.ViewSet):
class UsersViewSet(
        EnsureCsrfCookieMixin,
        viewsets.ModelViewSet
):
    """Users"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    # def list(self, request):
        # todo = Todo.objects.all()
        # serializer = TodoSerializer(todo, many=True)
        # if request.user.is_authenticated:  # and not request.user.is_lazy:
        #     return HttpResponseRedirect(reverse("index", host=c['host'].name))
        # else:
        #     return self.render_to_response(c, status=c['status'])
        # return Response([])

    # @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf])
    @action(
        methods=['post', 'get'],
        detail=False,
        permission_classes=[AllowAny]
    )
    def login(self, request):
        "Login using email and password."
        if request.user.is_authenticated:
            self.serializer_class = UserSerializer
            # serializer = UserSerializer(instance=self.queryset, many=False)
            # return Response(serializer.data)
            return Response(UserSerializer(request.user).data)

        self.serializer_class = LoginSerializer
        if request.method == 'POST':
            serializer = self.serializer_class(data=request.POST)
            record = LoginAttempt(ip=get_client_ip(request))
            if serializer.is_valid():
                user = serializer.validated_data['user']
                login(request, user)
                record.user = user
                record.save()
                return Response(UserSerializer(user).data)
            else:
                log.debug('LOGIN FAILED. Errors:')
                log.debug(serializer.errors)
                record.login = serializer.validated_data.get('email')
                record.password = serializer.validated_data.get('password')
                record.save()
                return Response({'errors': serializer.errors})
        else:
            return Response({})

    @action(methods=['post', 'get'], detail=False)
    def logout(self, request):
        logout(request)
        return Response({})
