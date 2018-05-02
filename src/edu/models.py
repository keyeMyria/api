from unidecode import unidecode
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import (
    pre_save,
    # post_save
)
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
# from django.contrib.sites.shortcuts import get_current_site
from django.contrib.postgres.fields import JSONField
from django.template.defaultfilters import slugify
from core.models import Tree
# from core.models import AddedChanged
# from core import now


class Category(Tree):
    """Task category (tree item)"""
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

    def __str__(self):
        if self.parent:
            return "{} > {}".format(self.parent, self.name)
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
        return '//ege.pashinin.com'

    def __str__(self):
        return self.title


class Organization(models.Model):
    """Educational organization (school / university)"""
    title = models.CharField(
        max_length=130,
        # verbose_name=_('Comment'),
        help_text='Example: "Bauman MSTU"',
    )
    location_str = models.CharField(
        max_length=130,
        blank=True, null=True,
        help_text='Example: "Россия, Москва"',
    )

    def __str__(self):
        return self.title


class Faculty(models.Model):
    """University Faculty.

    ex: факультет ИУ

    Faculty vs Department:

    The distinction between "faculty," "department," and "school"
    depends a lot on where you are. As Peter suggests in his answer, a
    faculty can be a collection of "departments." However, a faculty in
    Germany (for instance) consists of a number of "chairs," each of
    which is closer to a professorship in a department than an actual
    "department." Thus, the faculty is effectively halfway between the
    American "department" and "faculty" in its function, as it combines
    some of the hierarchy and responsibilities of each.

    """
    code = models.CharField(
        max_length=10,
        verbose_name='Код факультета',
        help_text="Например: ИУ",
    )
    title = models.CharField(
        max_length=130,
        verbose_name='Название факультета',
        help_text="Например: Информатики и систем управления",
    )
    university = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="faculties",
        help_text="University this faculty belongs to",
    )
    published = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_('Published'),
    )
    added = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        # verbose_name = "Предмет"
        # verbose_name_plural = "Предметы"
        unique_together = (
            # There may be no code at all, disabled:
            # ("code", "university"),
            ("title", "university"),
        )

    # @property
    # def departments(self):
    #     return self.department_set.all()

    def __str__(self):
        if self.code:
            return f'{self.title} ({self.code})'
        return self.title


class Department(models.Model):
    """University Department (Кафедра).

    ORG->Department
    or
    ORG->Faculty->Department

    ex.: Бауманка -> факультет ИУ -> ИУ2 ...

    Faculty vs Department:

    The distinction between "faculty," "department," and "school"
    depends a lot on where you are. As Peter suggests in his answer, a
    faculty can be a collection of "departments." However, a faculty in
    Germany (for instance) consists of a number of "chairs," each of
    which is closer to a professorship in a department than an actual
    "department." Thus, the faculty is effectively halfway between the
    American "department" and "faculty" in its function, as it combines
    some of the hierarchy and responsibilities of each.

    """

    code = models.CharField(
        max_length=10,
        blank=True, null=True,
        help_text="код полностью (ИУ2)",
    )
    code_slug = models.CharField(
        max_length=50,
        blank=True, null=True,
        help_text="url-valid code",
    )
    title = models.CharField(
        max_length=130,
        help_text="",
    )
    university = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="departments",
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="departments",
    )
    practice_comments_text = models.TextField(
        blank=True,
        null=True,
    )
    botva_links = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Department)
def department_pre_save(instance, *args, **kwargs):
    # TODO: handle redirects when renaming
    instance.code_slug = slugify(unidecode(instance.code))


class Period(models.Model):
    """A period of time for a student in current Department.

    Chosen by students. Can be whatever fits them:

    Year / Semester / Trimester / Quarter

    """
    slug = models.CharField(
        max_length=50,
    )
    name = models.CharField(
        max_length=100,
        help_text="Семестр 1",
    )
    department = models.ForeignKey(
        Department,
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name="periods",
    )

    class Meta:
        # verbose_name = "Предмет"
        # verbose_name_plural = "Предметы"
        unique_together = ("name", "department")

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Period)
def period_pre_save(instance, *args, **kwargs):
    # TODO: handle redirects when renaming
    instance.slug = slugify(unidecode(instance.name))


class Course(models.Model):
    """A course like "Java Programming"."""
    code = models.CharField(
        max_length=10,
        blank=True, null=True,
        help_text="код полностью (MPCS 51036)",
    )
    title = models.CharField(
        max_length=130,
        help_text="Java Programming",
    )
