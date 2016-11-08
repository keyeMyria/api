import datetime
import json
from core.views import BaseView
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse
from .forms import Enroll
from django.core.mail import send_mail
# from raven.contrib.django.raven_compat.models import client


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
            body = "{}\nИмя: {}\nТелефон: {}\n\n{}".format(
                datetime.datetime.now(),
                f.cleaned_data['name'],
                f.cleaned_data['phone'],
                f.cleaned_data['message']
            )
            send_mail(
                "Заявка от {}, тел.: {}".format(
                    f.cleaned_data['name'],
                    f.cleaned_data['phone']
                ),
                body,
                "{} <ROBOT@pashinin.com>".format(f.cleaned_data['name']),
                ["sergey@pashinin.com"])
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
