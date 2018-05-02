import urllib
import json
import logging
# from django.conf import settings
# from .models import Subject, Exam, Task
from core import now
# from edu.models import Task as EDUTask
from .models import Task
import pymorphy2
# from django.core.urlresolvers import reverse
from django.http import JsonResponse
from core import reverse
# from braces import views
from core.views import BaseView


morph = pymorphy2.MorphAnalyzer()
log = logging.getLogger(__name__)


class Base(
        # views.LoginRequiredMixin,
        # views.SuperuserRequiredMixin,
        BaseView
):

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['katex'] = True

        c['year'] = kwargs.get('year', None)
        if not c['year']:
            c['year'] = c.get('now', now()).year

        # c["host"] = self.request.host

        # c['EGE'] = settings.SITE_ID == 2
        c['EGE'] = self.request.host.name == 'ege'
        c['OGE'] = self.request.host.name == 'oge'
        c['exam_type'] = 0 if c['EGE'] else 1
        c['exam_type_str'] = 'ЕГЭ' if c['EGE'] else 'ОГЭ'

        c['menu']['index'] = {
            'title': 'Задачи',
            'url': reverse('index', host=c['host'].name),
            'hint': ''
        }
        c['menu'].current = 'index'

        # c['menu']['add'] = {
        #     'title': 'Добавить задачу',
        #     'url': reverse('index', host=c['host'].name),
        #     'hint': ''
        # }

        # c['subjects'] = Subject.objects.filter(published=True) \
        #                                .order_by('name')
        # for subj in c['subjects']:
        #     c['menu'][subj.slug] = {
        #         'title': subj.name,
        #         'url': reverse(
        #             'subject:index',
        #             host=c['host'].name,
        #             kwargs={
        #                 'subj': subj.slug,
        #             }
        #         ),
        #     }

        # c['menu'] = Menu(
        #     [
        #         ('index', {
        #             'title': 'Главная',
        #             'url': reverse('index'),
        #         }),
        #         ('articles', {
        #             'title': 'Статьи',
        #             'url': reverse('articles:index'),
        #         } if c['user'].is_superuser else None),
        #         ('faq', {
        #             'title': 'Вопросы',
        #             'url': reverse('faq'),
        #         }),
        #         ('contacts', {
        #             'title': 'Контакты',
        #             'url': reverse('contacts'),
        #         }),
        #     ]
        # )
        return c


class Tasks(Base):
    template_name = "edu_tasks_index.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['tasks'] = Task.objects.filter(published=True)
        # c['subjects'] = Subject.objects.filter(published=True) \
        #                                .order_by('name')
        return c

    def post(self, request, **kwargs):
        s = request.body.decode('utf-8')
        # print(s)
        # d = urllib.parse.parse_qs(s)
        d = json.loads(s)
        return JsonResponse(d)
        # from .forms import AddFacultyForm
        # f = AddFacultyForm(request.POST)
        # if f.is_valid():
        #     # Channel('send-me-lead').send(f.cleaned_data)
        #     return JsonResponse({
        #         'code': 0
        #     })
        # else:
        #     return JsonResponse({
        #         'errors': f.errors,
        #     })
