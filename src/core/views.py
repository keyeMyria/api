from datetime import date
from django.views.generic import TemplateView
from django.conf import settings
from core import get_client_ip, is_mobile
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


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
        c['year'] = date.today().year
        c['user'] = self.request.user
        c['DEBUG'] = settings.DEBUG
        c['VAGRANT'] = settings.VAGRANT
        c['RAVEN_PUBLIC'] = settings.RAVEN_PUBLIC
        c['INSTALLED_APPS'] = settings.INSTALLED_APPS

        # libraries
        c["jquery"] = True
        c["corecss"] = True
        c["livereload"] = True
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
