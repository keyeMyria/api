from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models.aggregates import Count
from random import randint
from django.db import transaction
from django.core.urlresolvers import reverse


class Task(models.Model):
    """Any task. Anything that can be solved."""
    # subject = models.ForeignKey(
    #     'Subject',
    #     db_column='subject',
    #     verbose_name=_('Subject'),
    #     # verbose_name_plural = _("Subjects")
    # )
    title = models.CharField(
        max_length=65,
        help_text=_("Google displays first 50-60 characters of a title tag")
    )
    added = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
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
        blank=True,
        null=True,
    )
    # tags = ArrayField(
    #     models.CharField(max_length=100),
    #     blank=True,
    #     null=True,
    #     verbose_name = _('Tags')
    # )
    # tags = models.ManyToManyField(
    #     'Tag',
    #     blank=True,
    # )
    # categories = models.ManyToManyField(
    #     'Category',
    #     blank=True,
    #     through='TasksCategories',
    # )
    published = models.BooleanField(
        default=False,
        db_index=True,
        # help_text=_("Published in the DB?")
    )

    class Meta:
        # db_table = 'edu_tasks'
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    # def get_absolute_url(self):
    #     return reverse("edu:onlytask", kwargs={
    #         'id': self.pk
    #     })

    def __str__(self):
        return self.title
