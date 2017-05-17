from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse


class Exam(models.Model):
    """Информация об экзамене ЕГЭ/ОГЭ.

    Включая год, предмет, типы задач.

    """
    Types = (
        (0, 'ЕГЭ (11 кл)'),
        (1, 'ОГЭ (9 кл)'),
    )

    type = models.IntegerField(
        default=0,
        choices=Types,
        verbose_name='Тип экзамена'
    )
    year = models.IntegerField()
    time = models.IntegerField(
        default=None,
        blank=True,
        null=True,
        help_text=_("Отведённое время, мин")
    )
    subject = models.ForeignKey('Subject')
    info = models.TextField(
        blank=True,
        null=True,
        help_text=_("Сколько задач и каких? Сколько длится экзамен?")
    )

    # comment = models.CharField(
    #     max_length=200,
    #     blank=True,
    #     null=True,
    #     help_text=_("Что нового по этому предмету в этом году?")
    # )
    # variants = models.ManyToManyField(
    #     'edu.Variant',
    #     # through = 'EgeVariants',
    #     blank=True,
    #     # related_name = 'ege',
    # )
    # tasks = models.ManyToManyField(
    #     'ege.Task',
    #     # through='EgeTasktypes',
    #     blank=True,
    #     related_name='exams',
    # )
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Экзамен (ЕГЭ / ОГЭ)"
        verbose_name_plural = "Экзамены (ЕГЭ / ОГЭ)"
        unique_together = ("type", "year", "subject")

    @property
    def info_formatted(self):
        from rparser import article_render as A
        html, info = A(self.info)
        return html

    def __str__(self):
        if self.type == 0:
            return "ЕГЭ - {} {}".format(self.subject, self.year)
        else:
            return "ОГЭ - {} {}".format(self.subject, self.year)


@receiver(pre_save, sender=Exam)
def ege_pre_save(instance, *args, **kwargs):
    instance.info = instance.info.replace("\r\n", "\n")


class Subject(models.Model):
    """Предмет ЕГЭ/ОГЭ"""
    name = models.CharField(
        max_length=50,
        verbose_name=_('Name')
    )
    slug = models.SlugField(
        max_length=60,
        verbose_name="URL part",
        # editable=False,
    )
    # tasks = models.ManyToManyField(
    #     'edu.Task',
    #     # through = 'EgeVariants',
    #     blank=True,
    #     # related_name = 'ege',
    #     help_text="Все задачи, по этому предмету ЕГЭ/ОГЭ"
    # )
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        unique_together = ("name", "slug")

    def get_absolute_url(self):
        return reverse('subject:index', kwargs={'subj': self.slug})

    def __str__(self):
        return self.name


class Task(models.Model):
    """Тип задачи в ЕГЭ/ОГЭ

    Определяется набором тэгов задач. Иначе говоря - это связь модели
    ЕГЭ и всех подходящих задач из приложения "edu"

    """
    order = models.IntegerField(
        verbose_name='Номер задачи',
        help_text='Например: от 1 до 27',
    )
    exam = models.ForeignKey(
        'ege.Exam',
        on_delete=models.CASCADE,
        null=True,
        related_name="tasks",
    )

    topic = models.CharField(
        max_length=150,
        verbose_name='Тема',
        null=True, blank=True,
        help_text='Отображаемая тема этой задачи экзамена, если не указана, '
        'то будут использованы тэги',
    )

    tags = models.ManyToManyField(
        'edu.Category',
        verbose_name=_('Tags'),
        related_name='ege_tasks',  # to get Task types from Tag model
        help_text='Все категории, которые подходят для этой задачи в экзамене'
    )

    def examples(self, only_published=True):
        from edu.models import Task, Category
        categories = Category.objects.get_queryset_descendants(
            self.tags, include_self=True)
        # get_descendants
        # names_to_exclude = [o.name for o in objects_to_exclude]
        # Foo.objects.exclude(name__in=names_to_exclude)
        if only_published:
            return Task.objects.filter(
                tags__in=categories,
                published=True,
            )
        else:
            return Task.objects.filter(tags__in=categories)

    def __str__(self):
        if self.topic:
            return self.topic
        else:
            return "{}".format(
                ', '.join([str(item.name) for item in self.tags.all()])
            )
