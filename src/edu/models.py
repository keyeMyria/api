from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
# from django.contrib.sites.shortcuts import get_current_site
from django.contrib.postgres.fields import JSONField
from core.models import Tree


class Category(Tree):
    name = models.CharField(
        max_length=100,
        help_text="Тема задачи или уникальная метка "
        "(системы счисления, исполнитель РОБОТ)",
    )
    hint = models.CharField(
        max_length=100,
        null=True, blank=True,
        help_text="Чуть подробднее о задаче"
        "(Дана таблица, найти то-то)",
    )
    # subject = models.ForeignKey(
    #     'Subject',
    #     db_column='subject',
    #     verbose_name=_('Subject'),
    #     # verbose_name_plural = _("Subjects")
    #     null=True,
    #     blank=True,
    # )

    # class Meta:
    #     db_table = 'edu_task'

    def __str__(self):
        if self.parent:
            return f"{self.parent} > {self.name}"
        else:
            return self.name
        # if self.hint:
        #     return "{} ({})".format(self.name, self.hint)
        # else:
        #     return "{}".format(self.name)


class Task(models.Model):
    """Any task. Anything that can be solved."""

    # Solution status
    NO_SOLUTION = 0
    PARTLY_SOLVED = 1
    SOLVED = 2
    SOLUTION_CHOICES = (
        (NO_SOLUTION, _('No solution')),
        (PARTLY_SOLVED, _('Partly solved')),
        (SOLVED, _('Solved')),
    )

    # Taken from
    NO_SOURCE = 0
    FIPI_BANK = 1
    BAUMANKA = 2
    BOOK_INF_2017_leshiner = 3
    SOURCE_CHOICES = (
        (NO_SOURCE, _('No source')),
        (FIPI_BANK, _('ФИПИ, открытый банк заданий')),
        (BAUMANKA, 'из Бауманки'),
        (BOOK_INF_2017_leshiner,
         'Типовые тестовые задания (ИНФ), 2017, Лещинер В.Р.'),
    )

    comment = models.CharField(
        max_length=130,
        verbose_name=_('Comment'),
        blank=True, null=True,
        help_text="ВУЗ, факультет, экзамен / рубежный контроль",
    )
    # subject = models.ForeignKey(
    #     'Subject',
    #     db_column='subject',
    #     verbose_name=_('Subject'),
    #     # verbose_name_plural = _("Subjects")
    # )
    title = models.CharField(
        max_length=100,
        verbose_name=_('Title'),
        help_text=_("Google displays first 50-60 characters of a title tag"),
    )
    added = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Added'),
    )
    # cut = models.TextField(
    #     # verbose_name=_('Solution'),
    #     blank=True,
    #     null=True,
    # )
    text = models.TextField(
        verbose_name=_('Task')
    )
    # no_short_answer = models.BooleanField(
    #     db_index=True,
    #     blank=True,
    # )
    # answer = models.CharField(
    #     max_length=50,
    #     null=True,
    #     blank=True,
    #     help_text=_("Short answer (if possible)")
    # )
    # answer2 = models.CharField(
    #     max_length=20,
    #     null=True,
    #     blank=True,
    #     help_text=_("If there is more than 1 answer")
    # )
    solution = models.TextField(
        verbose_name=_('Solution'),
        blank=True, null=True,
    )
    solution_status = models.IntegerField(
        verbose_name=_('Solution status'),
        default=NO_SOLUTION,
        choices=SOLUTION_CHOICES,
    )
    taken_from = models.IntegerField(
        verbose_name=_('Source'),
        default=NO_SOURCE,
        choices=SOURCE_CHOICES,
    )
    # tags = ArrayField(
    #     models.CharField(max_length=100),
    #     blank=True,
    #     null=True,
    #     verbose_name = _('Tags')
    # )
    tags = models.ManyToManyField(
        'Category',
        blank=True,
        verbose_name=_('Tags'),
    )
    # categories = models.ManyToManyField(
    #     'Category',
    #     blank=True,
    #     through='TasksCategories',
    # )
    marked_solved_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="edu_solved_tasks",
        verbose_name=_('People who think they solved it'),
    )
    published = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_('Published'),
        # help_text=_("Published in the DB?")
    )
    debug = JSONField(
        default=dict,
        blank=True, null=True,
    )

    class Meta:
        # db_table = 'edu_tasks'
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    @property
    def as_html(self):
        # TODO: display as article
        from rparser import article_render
        html, info = article_render(self.text)
        return html

    def get_absolute_url(self):
        if settings.SITE_ID == 2:
            return reverse("task", kwargs={
                'id': self.pk
            })
        else:
            return '//ege.pashinin.com'

    def __str__(self):
        return self.title
