import logging
from core.views import BaseView
# from django.conf import settings
from .models import Subject, Exam, Task
from core import now
from edu.models import Task as EDUTask
import pymorphy2
# from django.core.urlresolvers import reverse
from core import reverse
from braces import views

morph = pymorphy2.MorphAnalyzer()
log = logging.getLogger(__name__)


class Base(
        views.LoginRequiredMixin,
        views.SuperuserRequiredMixin,
        BaseView):

    def get_context_data(self, **kwargs):
        c = super(Base, self).get_context_data(**kwargs)
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
            'title': 'ЕГЭ' if c['EGE'] else 'ОГЭ',
            'url': reverse('index', host=c['host'].name),
            'hint': 'Единый государственный экзамен' if c['EGE'] else
            'Основной государственный экзамен'
        }
        c['menu'].current = 'index'
        c['subjects'] = Subject.objects.filter(published=True) \
                                       .order_by('name')
        for subj in c['subjects']:
            c['menu'][subj.slug] = {
                'title': subj.name,
                'url': reverse(
                    'subject:index',
                    host=c['host'].name,
                    kwargs={
                        'subj': subj.slug,
                    }
                ),
            }
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


class Index(Base):
    template_name = "ege_index.jinja"

    def get_context_data(self, **kwargs):
        c = super(Index, self).get_context_data(**kwargs)
        c['subjects'] = Subject.objects.filter(published=True) \
                                       .order_by('name')
        return c


class YearView(Base):
    template_name = "ege_year.jinja"

    def get_context_data(self, **kwargs):
        c = super(YearView, self).get_context_data(**kwargs)
        c['year'] = kwargs.get('year', c.get('now', now()).year)
        c['tasks'] = EDUTask.objects.filter()
        return c


class SubjectView(Base):
    template_name = "ege_subject.jinja"

    def get_context_data(self, **kwargs):
        c = super(SubjectView, self).get_context_data(**kwargs)
        c['year'] = kwargs.get('year', None)
        if not c['year']:
            c['year'] = c.get('now', now()).year

        subj = kwargs['subj']  # from urls pattern
        try:
            c['subject'] = Subject.objects.get(
                slug=subj,
                published=True
            )
            c['menu'].current = subj
            # дательный падеж:
            c['po_subject'] = " ".join([
                morph.parse(w)[0].inflect({'datv'}).word
                for w in str(c['subject']).split()
            ]).lower()
        except Subject.DoesNotExist:
            c['redirect'] = reverse("index")
            c['ege'] = None
            return c
            # return HttpResponseRedirect(reverse("index"))

        c['tasks'] = []
        try:
            c['exam'] = Exam.objects.get(
                subject=c['subject'],
                year=c['year'],
                type=c['exam_type']
            )
            c['tasks'] = c['exam'].tasks.filter().order_by('order')
        except Exam.DoesNotExist:
            # c['redirect'] = reverse("index")
            # print('EGE.DoesNotExist')
            # c['subject'] = None
            c['exam'] = None
            c['status'] = 404

        return c


class TaskView(SubjectView):
    template_name = "ege_task_single.jinja"


class ExamTaskView(SubjectView):
    template_name = "ege_subject_exam_task.jinja"

    def get_context_data(self, **kwargs):
        c = super(ExamTaskView, self).get_context_data(**kwargs)
        id = kwargs.get('id', None)
        c['exam_task'] = Task.objects.get(pk=id)
        return c


class SubjectTheoryView(SubjectView):
    template_name = "ege_subject.jinja"


class SubjectTasks(SubjectView):
    template_name = "ege_subject_tasks.jinja"
