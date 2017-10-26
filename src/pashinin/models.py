from core import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.core.urlresolvers import reverse
from channels.binding.websockets import WebsocketBinding
from ordered_model.models import OrderedModel
from django.conf import settings


class Course(models.Model):
    logo_sha1 = models.CharField(
        max_length=40,
        blank=True, null=True,
        default=None
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        blank=False, null=False,
        help_text="python-base, ege-inf, lpic-1, ...",
    )
    name = models.CharField(
        max_length=150,
        verbose_name=_('Name')
    )
    desc = models.TextField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    prereq = models.TextField(blank=True, null=True)
    program = models.TextField(blank=True, null=True)
    time_cost = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # not all sites have "/article/..." in urls
        # if settings.SITE_ID == 1:  # pashinin.com
        return reverse("courses:course", kwargs={
            'slug': self.slug
        })


class CourseBinding(WebsocketBinding):
    model = Course
    stream = "courses"
    fields = ["name", "desc"]

    @classmethod
    def group_names(cls, *args, **kwargs):
        return ["binding.values"]

    def has_permission(self, user, action, pk):
        return True


class CourseLead(models.Model):
    statuses = (
        (0, 'заявка создана (не обработана)'),
        (1, 'отменено'),
        (2, 'спам'),
        (3, 'время подтверждено'),
        (4, 'я не дозвонился до клиента'),
    )
    status = models.IntegerField(
        default=0,
        choices=statuses,
        verbose_name='Статус'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='leads',
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True
        # related_name='courses_enrolled',
    )
    name = models.CharField(
        max_length=150,
        verbose_name=_('Name'),
        blank=True, null=True
    )
    contact = models.CharField(
        max_length=150,
        verbose_name=_('Contact'),
        blank=True, null=True
    )
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} from {}".format(self.course, self.student)

    # class Meta:
    #     unique_together = ("course", "student")


class Lesson(models.Model):
    "Один конкретный урок в определенное время"

    statuses = (
        (0, 'назначено время'),
        (1, 'проведено'),
        (2, 'пропуск (предупредили минимум за 24 часа)'),
        (3, 'пропуск (без предупреждения или менее чем за 24ч)'),
    )
    status = models.IntegerField(
        default=0,
        choices=statuses,
        verbose_name='Статус'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='lessons',
    )
    start = models.DateTimeField(db_index=True)  # auto_now_add=True
    end = models.DateTimeField(db_index=True)
    comment = models.TextField(
        blank=True,
        null=True,
        help_text="Что было на этом занятии?"
    )
    scheduled = models.BooleanField(
        default=False,
        help_text="Повторяется ли это занятие? Время берется из поля start."
    )

    @property
    def empty(self):
        return not bool(self.student)

    @property
    def length(self):
        # .replace(tzinfo=None)
        return self.end - self.start

    @property
    def mins(self):
        return self.length.seconds // 60

    def __str__(self):
        #
        # return self.start.strftime("%Y-%m-%d %H:%M:%S")
        return self.start.isoformat()


class QA(OrderedModel):
    question = models.CharField(
        max_length=250,
        verbose_name=_('Question')
    )
    answer = models.TextField(blank=True, null=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
