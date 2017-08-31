import datetime
# import json
from core import json
from core.views import BaseView
from core.menu import Menu
from django.utils.timezone import now, localtime
# from django.utils.translation import ugettext as _
# from django.core.urlresolvers import reverse
from . import student_info
from core import reverse
# from django.conf import settings
from django.http import HttpResponse, Http404
# from django.contrib.auth.models import User
from .forms import Enroll, AddStudent, CourseEnrollForm
from .models import Lesson, CourseLead, Course
# from django.utils.decorators import method_decorator
# from raven.contrib.django.raven_compat.models import client
# from django.views.decorators.csrf import ensure_csrf_cookie
# from rest_framework.views import APIView
from channels import Channel
from braces import views
from django.contrib.auth import get_user_model
import logging

log = logging.getLogger(__name__)
User = get_user_model()


class Base(BaseView):
    def get_context_data(self, **kwargs):
        c = super(Base, self).get_context_data(**kwargs)
        c["phone"] = '+7 (977) 801-25-41'
        c["email"] = 'sergey@pashinin.com'
        c["price"] = 1000
        c["price45"] = 800
        c["menu_id"] = "services"

        c['menu'] = Menu(
            [
                ('index', {
                    'title': 'Главная',
                    'url': reverse('index'),
                }),
                ('articles', {
                    'title': 'Статьи',
                    'url': reverse('articles:index'),
                } if c['user'].is_superuser else None),
                ('faq', {
                    'title': 'Вопросы',
                    'url': reverse('faq'),
                }),
                ('contacts', {
                    'title': 'Контакты',
                    'url': reverse('contacts'),
                }),
                ('students', {
                    'title': 'Ученики',
                    'url': reverse('students'),
                } if c['user'].is_superuser else None),
            ]
        )
        return c


class Index(Base):
    template_name = "pashinin_index.jinja"

    def get_context_data(self, **kwargs):
        c = super(Index, self).get_context_data(**kwargs)
        # c["menu_id"] = "index"
        c["menu"].current = 'index'
        return c

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
        c["menu"].current = 'contacts'
        return c


def times():
    cur = datetime.timedelta(hours=10)
    end = datetime.timedelta(hours=21)
    while cur < end:
        yield (cur, cur+datetime.timedelta(hours=1))
        cur += datetime.timedelta(minutes=30, hours=1)


def prev_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0:  # Target day already happened this week
        days_ahead -= 7
    return d + datetime.timedelta(days_ahead)


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


class Week:
    pass


class Day:
    lesson_length = datetime.timedelta(minutes=60)
    lesson_length_s = lesson_length.total_seconds()
    start_time = datetime.time(10, 0, 0)
    end_time = datetime.time(22, 0, 0)
    pause = datetime.timedelta(minutes=30)
    len_plus_pause = lesson_length + pause

    def __init__(self, when):
        self.schedule = []

        if isinstance(when, datetime.datetime):
            self.start = self.end = self.date = when  # .date()
        else:
            self.start = self.end = self.date = localtime(now()).replace(
                year=when.year,
                month=when.month,
                day=when.day,
            )
        # self.start = datetime.datetime.combine(self.date, Day.start_time)
        # self.end = datetime.datetime.combine(self.date, Day.end_time)

        from pytz import timezone
        localtz = timezone('Europe/Moscow')
        self.start = self.start \
                         .replace(tzinfo=localtz) \
                         .replace(
                             hour=Day.start_time.hour,
                             minute=Day.start_time.minute,
                             second=0
                         )
        self.end = self.end.replace(tzinfo=localtz).replace(
            hour=self.end_time.hour,
            minute=0
        )

        # Monday       |     | Next day of week   |
        # future day 1 | ... | next_week_last_day | today | ...
        self.next_week_last_day = False

        # if there are no lessons planned - empty schedule
        if self.lessons.count() == 0:
            c = localtime(self.start)
            while c + Day.lesson_length < self.end:
                self.schedule.append(Lesson(
                    start=c,
                    end=(c + Day.lesson_length),
                    student=None
                ))
                c += Day.len_plus_pause

        # Iterate over created or scheduled lessons
        lessons = list(self.lessons)
        lessons.sort(key=lambda x: x.start.time())
        log.debug(lessons)
        for i, lesson in enumerate(lessons):
            lesson.start = lesson.start.replace(
                year=self.date.year,
                month=self.date.month,
                day=self.date.day,
            )
            lesson.end = lesson.end.replace(
                year=self.date.year,
                month=self.date.month,
                day=self.date.day,
            )

            first = i == 0
            last = i == len(self.lessons)-1

            # before first lesson
            if localtime(lesson.start).time() > Day.start_time and first:
                log.debug(lesson)
                L = Lesson(
                    start=self.start,
                    # end=localtime(lesson.start) - Day.pause,
                    end=localtime(lesson.start),
                    student=None
                )
                total = L.length.total_seconds()
                len1 = Day.lesson_length + Day.pause
                len1_s = len1.total_seconds()
                # print(total / len1_s)
                # count = math.floor(total / len1_s)
                count = round(total / len1_s)
                s = localtime(lesson.start) - \
                    (Day.lesson_length + Day.pause)*count
                for i in range(0, count):
                    self.schedule.append(Lesson(
                        start=s + len1*i,
                        end=s + len1*i + Day.lesson_length,
                        student=None
                    ))
                # Day.make_schedule(Day.start, lesson.start.time())
                self.schedule.append(lesson)

            # add empty lessons after last lesson
            if localtime(lesson.end).time() < Day.end_time and last:
                # L = Lesson(
                #     start=lesson.end,
                #     end=self.end,
                #     student=None
                # )
                # total = L.length.total_seconds()
                # len1 = Day.lesson_length + Day.pause
                # len1_s = len1.total_seconds()
                # count = round(total / len1_s)

                # c = lesson.end.replace(
                #     year=self.date.year,
                #     month=self.date.month,
                #     day=self.date.day,
                # ) + Day.pause
                c = localtime(lesson.end).replace(
                    year=self.date.year,
                    month=self.date.month,
                    day=self.date.day,
                ) + Day.pause
                while c.time() < self.end.time():
                    self.schedule.append(Lesson(
                        start=c,
                        end=c + Day.lesson_length,
                        student=None
                    ))
                    c += Day.lesson_length + Day.pause

                # s = self.end.replace(tzinfo=localtz).replace(
                #     hour=localtime(lesson.end).hour,
                #     # minutes=localtime(lesson.end).minutes
                # ) + Day.pause
                # for i in range(0, count):
                #     self.schedule.append(Lesson(
                #         start=s + len1*i,
                #         end=s + len1*i + Day.lesson_length,
                #         student=None
                #     ))
                # Day.make_schedule(Day.start, lesson.start.time())

            if not first and not last:
                self.schedule.append(lesson)

    @property
    def title(self):
        return 'asd'

    @property
    def lessons(self):
        """Lessons in this day + scheduled lessons."""
        a = (Lesson.objects.filter(
            start__year=self.date.year,
            start__month=self.date.month,
            start__day=self.date.day,
        ) | Lesson.objects.filter(
            scheduled=True,
            start__week_day=self.date.weekday()+2
            # why + 2?
            # TODO
            # python weekday starts from 0 (sunday) to 6 (saturday)
        ))
        # .order_by("start__time__hour")
        # log.debug(Lesson.objects.filter(
        #     scheduled=True,
        #     start__week_day=self.date.weekday()+2
        # ))
        log.debug(a)
        return a

    def __str__(self):
        return str(self.date)


class CourseView(Base):
    template_name = "pashinin_course.jinja"

    def get_context_data(self, **kwargs):
        c = super(CourseView, self).get_context_data(**kwargs)
        try:
            c['course'] = Course.objects.get(slug=c['slug'])
        except:
            raise Http404

        if c['user'].is_authenticated:
            c['leads'] = CourseLead.objects.filter(
                student=c['user'],
                course=c['course']
            )
        else:
            c['leads'] = CourseLead.objects.filter(
                student=None,
                course=c['course'],
                session_key=self.request.session.session_key,
            )

        if c['leads'].count() > 0:
            c['lead'] = c['leads'][0]
            c['enrolled'] = c['lead'].status != 1
        else:
            c['lead'] = None
            c['enrolled'] = False
        return c

    def post(self, request, **kwargs):
        c = self.get_context_data(**kwargs)

        # cancel course enroll
        if 'cancel' == request.POST.get('action'):
            if c['user'].is_authenticated:
                lead = CourseLead.objects.get(
                    course=c['course'],
                    student=c['user']
                )
            else:
                if not request.session.session_key:
                    request.session.save()
                lead = CourseLead.objects.get(
                    course=c['course'],
                    session_key=request.session.session_key,
                    student=None
                )
            lead.status = 1
            lead.save()
            # TODO: change lead status to "cancelled by user"
            return HttpResponse(json.dumps({'code': 0}))

        # enroll here
        f = CourseEnrollForm(request.POST)
        if f.is_valid():
            data = f.json()
            data['course'] = c['slug']

            new_lead = True
            if c['user'].is_authenticated:
                lead, new_lead = CourseLead.objects.get_or_create(
                    course=c['course'],
                    student=c['user']
                )
            else:
                if not request.session.session_key:
                    request.session.save()
                lead, new_lead = CourseLead.objects.get_or_create(
                    course=c['course'],
                    session_key=request.session.session_key,
                    student=None
                )

            lead.name = data['name']
            lead.contact = data['contact']
            lead.comment = data['comment']
            if new_lead:
                Channel('course-enroll').send(data)
            else:
                if lead.status != 0:
                    lead.status = 0
                    lead.save()
            lead.save()
            return HttpResponse(json.dumps({'code': 0}))
        else:
            return HttpResponse(json.dumps({
                'errors': f.errors,
            }))


class Students(views.LoginRequiredMixin,
               views.SuperuserRequiredMixin,
               Base):
    template_name = "pashinin_students.jinja"

    # active students have a last lesson within a week
    last_lesson_period = datetime.timedelta(days=8)

    def get_context_data(self, **kwargs):
        c = super(Students, self).get_context_data(**kwargs)
        utcnow = localtime(now())
        c["momentjs"] = True
        c['timeago'] = True
        c['dragula'] = True

        c['students'] = {
            'active': User.objects.filter(
                lessons__start__gt=utcnow-self.last_lesson_period
                # start__year=self.date.year,
                # start__month=self.date.month,
                # start__day=self.date.day,
            ),
            'inactive': User.objects.filter(
                lessons__start__lte=utcnow-self.last_lesson_period
            )
        }
        c['pause_mins'] = Day.pause.seconds // 60
        c["menu"].current = 'students'
        # utcnow = datetime.datetime.utcnow()

        # django.utils.timezone.now()
        c['monday'] = next_weekday(utcnow, 0)
        c['today'] = Day(utcnow)
        c['days'] = []
        c['days'] += [
            # {
            #     'weekday': datetime.date(2001, 1, i+1).weekday(),
            #     'datetime': utcnow + datetime.timedelta(days=7),
            # }
            Day(c['monday'] + datetime.timedelta(days=i))
            # datetime.date(2001, 1, i).strftime('%A'),
            # c['monday'] + datetime.timedelta(days=i),
            # datetime.date(2001, 1, i+1).weekday(),
            for i in range(0, utcnow.weekday())
        ]
        if c['days']:
            c['days'][-1].next_week_last_day = True

        c['days'] += [
            Day(utcnow + datetime.timedelta(days=i))
            for i in range(0, 7-utcnow.weekday())
        ]
        c['times'] = [item for item in times()]
        return c

    def post(self, request, **kwargs):
        # c = self.get_context_data(**kwargs)
        f = AddStudent(request.POST)
        utcnow = localtime(now())

        return HttpResponse(
            json.dumps([student_info(u) for u in User.objects.filter(
                lessons__start__gt=utcnow-self.last_lesson_period
            )]),
            content_type='application/json'
        )

        if f.is_valid():
            # new_user = User.objects.create(is_active=False)
            # new_user.save()
            # Channel('send-me-lead').send(f.json())
            return HttpResponse(
                json.dumps({'code': 0}),
                content_type='application/json'
            )
        else:
            return HttpResponse(
                json.dumps({
                    'errors': f.errors,
                }), content_type='application/json'
            )
        # return HttpResponse(json.dumps({
        #     'url': 'f.get_absolute_url()',
        #     'id': 'f.pk',
        #     'sha1': 'f.sha1'
        # }), content_type='application/json')


class FAQ(Base):
    template_name = "pashinin_faq.jinja"

    def get_context_data(self, **kwargs):
        c = super(FAQ, self).get_context_data(**kwargs)
        c["exp"] = datetime.datetime.now() - datetime.datetime(2013, 1, 1)
        c["menu"].current = 'faq'
        return c
