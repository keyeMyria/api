from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.core.urlresolvers import reverse
from django.conf import settings


class Course(models.Model):
    slug = models.SlugField(max_length=60, unique=True)
    name = models.CharField(
        max_length=150,
        verbose_name=_('Name')
    )
    desc = models.TextField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    prereq = models.TextField(blank=True, null=True)
    program = models.TextField(blank=True, null=True)
    time_cost = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


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
    session_key = models.CharField(
        max_length=150,
        # verbose_name='session_key'
        blank=True, null=True
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
        if self.student:
            return "{} from {}".format(self.course, self.student)
        else:
            return "{} from {}".format(self.course, self.session_key)

    class Meta:
        unique_together = ("course", "session_key", "student")


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

#     year = models.IntegerField()
#     subject = models.ForeignKey('Subject')

#     comment = models.TextField(
#         blank=True,
#         null=True,
#         help_text=_("Сколько задач и каких? Сколько длится экзамен?")
#     )

#     # variants = models.ManyToManyField(
#     #     'edu.Variant',
#     #     # through = 'EgeVariants',
#     #     blank=True,
#     #     # related_name = 'ege',
#     # )
#     # tasks = models.ManyToManyField(
#     #     'ege.Task',
#     #     # through='EgeTasktypes',
#     #     blank=True,
#     #     related_name='exams',
#     # )
#     published = models.BooleanField(default=False)

#     class Meta:
#         verbose_name = _("ЕГЭ / ОГЭ")
#         verbose_name_plural = _("ЕГЭ / ОГЭ")
#         unique_together = ("type", "year", "subject")

#     @property
#     def info_formatted(self):
#         from rparser import article_render as A
#         html, info = A(self.info)
#         return html

#     def __str__(self):
#         if self.type == 0:
#             return "ЕГЭ - {} {}".format(self.subject, self.year)
#         else:
#             return "ОГЭ - {} {}".format(self.subject, self.year)


# @receiver(pre_save, sender=Exam)
# def ege_pre_save(instance, *args, **kwargs):
#     instance.info = instance.info.replace("\r\n", "\n")


# class Subject(models.Model):
#     """Предмет ЕГЭ/ОГЭ"""
#     name = models.CharField(
#         max_length=50,
#         verbose_name=_('Name')
#     )
#     slug = models.SlugField(
#         max_length=60,
#         verbose_name="URL part",
#         # editable=False,
#     )
#     # tasks = models.ManyToManyField(
#     #     'edu.Task',
#     #     # through = 'EgeVariants',
#     #     blank=True,
#     #     # related_name = 'ege',
#     #     help_text="Все задачи, по этому предмету ЕГЭ/ОГЭ"
#     # )
#     published = models.BooleanField(default=False)

#     class Meta:
#         verbose_name = "Предмет"
#         verbose_name_plural = "Предметы"
#         unique_together = ("name", "slug")

#     def get_absolute_url(self):
#         return reverse('subject:index', kwargs={'subj': self.slug})

#     def __str__(self):
#         return self.name


# class Task(models.Model):
#     """Тип задачи в ЕГЭ/ОГЭ

#     Определяется набором тэгов задач. Иначе говоря - это связь модели
#     ЕГЭ и всех подходящих задач из приложения "edu"

#     """
#     order = models.IntegerField(
#         verbose_name='Номер задачи',
#         help_text='Например: от 1 до 27',
#     )
#     exam = models.ForeignKey(
#         'ege.Exam',
#         on_delete=models.CASCADE,
#         null=True,
#         related_name="tasks",
#     )

#     topic = models.CharField(
#         max_length=150,
#         verbose_name='Тема',
#         null=True, blank=True,
#         help_text='Отображаемая тема этой задачи экзамена, если не указана, '
#         'то будут использованы тэги',
#     )

#     Type = (
#         (0, '1 единственная задача'),
#         (1, '1 задача из N на выбор'),

#         # или больше, в этом случае в модели ЕГЭ должны повторяться
#         # записи Task с одинаковыми полями "order".  То есть больше
#         # одной задачи с одним и тем же порядковым номером
#     )
#     type = models.IntegerField(
#         default=0,
#         choices=Type,
#         verbose_name='Нужно решить'
#     )
#     tags = models.ManyToManyField(
#         'edu.Tag',
#         verbose_name=_('Tags'),
#         related_name='ege_tasks',  # to get Task types from Tag model
#        help_text='Все тэги, которые подходят для этой задачи в этом экзамене'
#     )

#     def __str__(self):
#         if self.topic:
#             return self.topic
#         else:
#             return "{}".format(
#                 ', '.join([str(item.name) for item in self.tags.all()])
#             )
