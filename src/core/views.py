import os
import json
import logging
from datetime import date
from django.views.generic import TemplateView
from django.conf import settings
from core import get_client_ip, is_mobile
from django.utils.translation import ugettext as _
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.cache import cache
from subprocess import call, Popen, PIPE
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from .models import SiteUpdate

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
class BaseView(TemplateView):
    only_superuser = False

    def get_context_data(self, **kwargs):
        c = super(BaseView, self).get_context_data(**kwargs)
        c["domain"] = settings.DOMAIN
        c['year'] = date.today().year
        c['user'] = self.request.user
        c['DEBUG'] = settings.DEBUG
        c['RAVEN_PUBLIC'] = settings.RAVEN_PUBLIC
        c['INSTALLED_APPS'] = settings.INSTALLED_APPS

        # libraries
        c["jquery"] = True
        c["corecss"] = True
        c["chartjs"] = False
        c["nouislider"] = False
        c["dropzone"] = c['user'].is_superuser
        c['lng'] = 'en' if self.request.LANGUAGE_CODE in ('en', 'en-us')\
                   else 'ru'

        try:
            c['o'] = settings.OPTIONS
        except:
            c['o'] = {}
        c['ip'] = get_client_ip(self.request)
        c["analytics"] = not (
            c['user'].is_superuser or
            c['ip'] in (
                '10.254.239.2',
                '10.92.209.1',
            ))
        c['status'] = 200
        c['mobile'] = is_mobile(self.request)
        return c

    def get(self, request, **kwargs):
        c = self.get_context_data(**kwargs)

        # Redirects
        redirect = c.get("redirect", None)
        if redirect:
            return HttpResponseRedirect(redirect)

        # Pages for superuser only
        if self.only_superuser and not c['user'].is_superuser:
            return HttpResponseNotFound('')

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


class Celery(BaseView):
    template_name = "core_celery.jinja"
    only_superuser = True

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


class Updates(BaseView):
    template_name = "core_updates.jinja"
    only_superuser = True

    def get_context_data(self, **kwargs):
        c = super(Updates, self).get_context_data(**kwargs)
        c["timeago"] = True
        c["updates"] = SiteUpdate.objects.filter().order_by('-started')
        return c


class Nginx(BaseView):
    template_name = "core_nginx.jinja"
    only_superuser = True

    def get_context_data(self, **kwargs):
        c = super(Nginx, self).get_context_data(**kwargs)
        try:
            p = Popen(['nginx', '-V'])
            nginxv, err = p.communicate(stdout=PIPE)
        except:
            nginxv = '''nginx version: nginx/1.10.0 (Ubuntu)
built with OpenSSL 1.0.2g  1 Mar 2016
TLS SNI support enabled
configure arguments: --with-cc-opt='-g -O2 -fPIE -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2' --with-ld-opt='-Wl,-Bsymbolic-functions -fPIE -pie -Wl,-z,relro -Wl,-z,now' --prefix=/usr/share/nginx --conf-path=/etc/nginx/nginx.conf --http-log-path=/var/log/nginx/access.log --error-log-path=/var/log/nginx/error.log --lock-path=/var/lock/nginx.lock --pid-path=/run/nginx.pid --http-client-body-temp-path=/var/lib/nginx/body --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-proxy-temp-path=/var/lib/nginx/proxy --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --with-debug --with-pcre-jit --with-ipv6 --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-http_auth_request_module --with-http_addition_module --with-http_dav_module --with-http_geoip_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_image_filter_module --with-http_v2_module --with-http_sub_module --with-http_xslt_module --with-stream --with-stream_ssl_module --with-mail --with-mail_ssl_module --with-threads --add-module=/build/nginx-pzhfc2/nginx-1.10.0/debian/modules/nginx-auth-pam --add-module=/build/nginx-pzhfc2/nginx-1.10.0/debian/modules/nginx-dav-ext-module --add-module=/build/nginx-pzhfc2/nginx-1.10.0/debian/modules/nginx-echo --add-module=/build/nginx-pzhfc2/nginx-1.10.0/debian/modules/nginx-upstream-fair --add-module=/build/nginx-pzhfc2/nginx-1.10.0/debian/modules/ngx_http_substitutions_filter_module'''

        c["nginxv"] = nginxv
        c["arguments"] = nginxv
        return c


# def err404(request):
#     if request.method == 'GET':
#         return HttpResponseNotFound(render_to_string('404.html', locals()))
#     else:
#         return HttpResponseNotFound('404')


# def err500(request):
#     if request.method == 'GET':
#         return HttpResponseServerError(render_to_string('500.html', locals()))
#     else:
#         return HttpResponseServerError('500')

class Logout(APIView):
    def get(self, request, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

    def post(self, request, **kwargs):
        logout(request)
        return HttpResponse("{}")
