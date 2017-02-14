from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
# from django.contrib.sites.shortcuts import get_current_site
from django.contrib.postgres.fields import JSONField


class Task(models.Model):
    """Any task. Anything that can be solved."""
    # subject = models.ForeignKey(
    #     'Subject',
    #     db_column='subject',
    #     verbose_name=_('Subject'),
    #     # verbose_name_plural = _("Subjects")
    # )
    title = models.CharField(
        max_length=100,
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
        return 'TODO'

    def get_absolute_url(self):
        if settings.SITE_ID == 2:
            return reverse("task", kwargs={
                'id': self.pk
            })
        else:
            return '//ege.pashinin.com'

    def __str__(self):
        return self.title
