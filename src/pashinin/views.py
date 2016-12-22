import datetime
import json
from core.views import BaseView
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse
from .forms import Enroll
from core.forms import Login as LoginForm
from django.http import HttpResponseRedirect
# from django.utils.decorators import method_decorator
# from raven.contrib.django.raven_compat.models import client
from django.contrib.auth import login
# from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token
from rest_framework.views import APIView
from django.contrib.auth import logout
from core.views import EnsureCsrfCookieMixin
from channels import Channel


class Base(BaseView):
    def get_context_data(self, **kwargs):
        c = super(Base, self).get_context_data(**kwargs)
        c["phone"] = '+7 (977) 801-25-41'
        c["email"] = 'sergey@pashinin.com'
        c["price"] = 900
        c["price45"] = 700
        c["menu_id"] = "services"
        c['menu'] = {
            'parent': None,
            'items': [
                {
                    'title': 'Главная',
                    'url': reverse('index'),
                },
                {
                    'title': 'Статьи',
                    'url': reverse('articles:index'),
                } if c['user'].is_superuser else None,
                {
                    'title': 'Вопросы',
                    'url': reverse('faq'),
                },
                {
                    'title': 'Контакты',
                    'url': reverse('contacts'),
                },
            ]
        }
        return c


class Index(Base):
    template_name = "pashinin_index.jinja"

    def post(self, request, **kwargs):
        f = Enroll(request.POST)
        if f.is_valid():
            Channel('send-me-lead').send(f.json())
            return HttpResponse(json.dumps({'code': 0}))
        else:
            return HttpResponse(json.dumps({
                'errors': f.errors,
            }))


class Contacts(Base):
    template_name = "pashinin_contacts.jinja"

    def get_context_data(self, **kwargs):
        c = super(Contacts, self).get_context_data(**kwargs)
        c["menu_id"] = "contacts"
        return c


class FAQ(Base):
    template_name = "pashinin_faq.jinja"

    def get_context_data(self, **kwargs):
        c = super(FAQ, self).get_context_data(**kwargs)
        c["exp"] = datetime.datetime.now() - datetime.datetime(2013, 1, 1)
        return c


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class Login(EnsureCsrfCookieMixin, Base):
    template_name = "pashinin_login.jinja"

    def get_context_data(self, **kwargs):
        c = super(Login, self).get_context_data(**kwargs)
        c['menu'] = {}
        # c['form'] = LoginForm
        return c

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            c = self.get_context_data(**kwargs)
            return self.render_to_response(c, status=c['status'])

    def post(self, request, **kwargs):
        f = LoginForm(request.POST)
        # request.GET.get('redirect')
        # Check form input data (email and password)
        if f.is_valid():
            login(request, f.cleaned_data['user'])
            return HttpResponse(json.dumps({'code': 0}))
        else:
            return HttpResponse(json.dumps({
                'errors': f.errors,
            }))


class Logout(APIView):
    def post(self, request, **kwargs):
        logout(request)
        return HttpResponse("{}")
