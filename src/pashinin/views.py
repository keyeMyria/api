import datetime
import json
from core.views import BaseView
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse
from .models import P
from .forms import Enroll
from django.core.mail import send_mail
# from raven.contrib.django.raven_compat.models import client


class Base(BaseView):
    def get_context_data(self, **kwargs):
        c = super(Base, self).get_context_data(**kwargs)
        c["phone"] = settings.PHONE
        c["email"] = settings.EMAIL
        c["price"] = settings.PRICE
        c["price45"] = settings.PRICE45
        c["P"] = P
        c["menu_id"] = "services"
        c['menu'] = {
            'parent': None,
            'items': [
                {
                    'title': 'Главная',
                    'url': reverse('index'),
                },
                {
                    'title': 'Контакты',
                    'url': reverse('contacts')
                },
            ]
        }
        return c


# class Services(Base):
#     template_name = "services.jinja"

#     def get_context_data(self, **kwargs):
#         c = super(Services, self).get_context_data(**kwargs)
#         h = datetime.now().hour
#         if h >= 20 or h <= 9:
#             c["contact1"] = 'sergey@pashinin.com'
#         return c

#     def get(self, request, **kwargs):
#         vars = self.get_context_data()
#         return self.render_to_response(vars, **kwargs)


class IT(Base):
    template_name = "repetitor_it.jinja"

    # def get_context_data(self, **kwargs):
    #     c = super(IT, self).get_context_data(**kwargs)
    #     return c

    def post(self, request, **kwargs):
        f = Enroll(request.POST)
        if f.is_valid():
            send_mail("Заявка от {}, тел.: {}".format(
                f.cleaned_data['name'],
                f.cleaned_data['phone']
            ),
                      "{}\nИмя: {}\nТелефон: {}\n\n{}".format(datetime.datetime.now(),
                          f.cleaned_data['name'],
                          f.cleaned_data['phone'],
                          f.cleaned_data['message']),
                      "{} <ROBOT@pashinin.com>".format(f.cleaned_data['name']),
                      ["sergey@pashinin.com"])
            return HttpResponse(json.dumps({
                'code': 0,
            }))
        else:
            return HttpResponse(json.dumps({
                'errors': f.errors,
            }))


# class Blog(Base):
#     template_name = "articles.jinja"

#     def get_context_data(self, **kwargs):
#         c = super(Blog, self).get_context_data(**kwargs)
#         c['articles'] = Article.objects.filter()
#         c['changed'] = Article.objects.filter().order_by('-changed_on')[:10]
#         c['timeago'] = True
#         c["menu_id"] = "articles"
#         return c

    # def get(self, request, **kwargs):
    #     c = self.get_context_data(**kwargs)
    #     return self.render_to_response(c)


class Contacts(Base):
    template_name = "contacts.jinja"

    def get_context_data(self, **kwargs):
        c = super(Contacts, self).get_context_data(**kwargs)
        c["menu_id"] = "contacts"
        return c
