from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse


class EGE(models.Model):
    """Информация об экзамене ЕГЭ/ОГЭ.

    Включая год, предмет, типы задач.

    """
    ExamType = (
        (0, 'ЕГЭ (11 кл)'),
        (1, 'ОГЭ (9 кл)'),
    )

    type = models.IntegerField(
        default=0,
        choices=ExamType,
        verbose_name='Тип экзамена'
    )
    year = models.IntegerField()
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
    #     'edu.Category',
    #     through='EgeTasktypes',
    #     blank=True,
    #     # related_name = 'ege',
    # )
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("ЕГЭ / ОГЭ")
        verbose_name_plural = _("ЕГЭ / ОГЭ")
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


@receiver(pre_save, sender=EGE)
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
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        unique_together = ("name", "slug")

    def get_absolute_url(self):
        return reverse('subject', kwargs={'subj': self.slug})

    def __str__(self):
        return self.name
