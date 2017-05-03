from django.core.exceptions import ImproperlyConfigured
try:
    from rparser import article_render
except:
    raise ImproperlyConfigured('Run: "pip install rparser"')


from django.db import models
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
# from dirtyfields import DirtyFieldsMixin
# from elasticsearch import Elasticsearch
from unidecode import unidecode
from core.models import AddedChanged
# import bleach
from django.utils.translation import gettext_lazy as _
# from raven.contrib.django.raven_compat.models import client
import logging
log = logging.getLogger(__name__)


# class ArticleCategory(Debug, Tree, Translated):
#     title = models.CharField(
#         max_length=765,
#         verbose_name=_("Title")
#     )

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name = _('Category')
#         verbose_name_plural = _('Categories')


# class Article(DirtyFieldsMixin, Approved, AddedChanged, Debug, Translated):
class Article(AddedChanged):
    title = models.CharField(
        max_length=765,
        verbose_name=_("Title")
    )
    src = models.TextField(
        default=None,
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        max_length=765,
        verbose_name="In URL",
        default=None,
        null=True,
        editable=False,
        blank=True,
        help_text="/articles/.../how-to-install-linux"
    )
    author = models.ForeignKey(
        'core.User',
        default=None,
        null=True,
        blank=True
    )
    published = models.BooleanField(
        default=False,
        db_index=True,
        # help_text=_("Published in the DB?")
    )

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        # unique_together = (("page_namespace", "title"),)
        # index_together = [["name", "domain"], ]

    def get_absolute_url(self):
        # print(get_current_site(request))
        # not all sites have "/article/..." in urls
        # if settings.SITE_ID == 1:  # pashinin.com
        return reverse("articles:article", kwargs={
            'id': self.pk,
            'slug': self.slug
        })

    def get_header(self):
        if self.header:
            return self.header
        self.header = strip_tags(self.html)[:265]
        self.save()
        return self.header

    @property
    def as_html(self):
        try:
            html, info = article_render(self.src)

            missing_links = info.get("missing_links", tuple())
            set_links = {}
            if missing_links:
                for missing_page in missing_links:
                    slug = slugify(unidecode(missing_page))
                    try:
                        article = Article.objects.get(slug=slug)
                        set_links[missing_page] = article.get_absolute_url()
                    except:
                        print("no page:", slug)
            return html
        except Exception as e:
            # TODO
            msg_debug = "Article.as_html error: " + str(e)
            if settings.DEBUG:
                log.error(msg_debug)
                return msg_debug
            else:

                return "Error happened! I know about it."

    @property
    def as_latex(self):
        return "TODO: Article.as_latex property"

    @property
    def is_redirect(self):
        "TODO"
        return None

    # @property
    # def tags(self):
    #     return []

    # @classmethod
    # def untagged(cls, namespace=0):
    #     """Get pages that do not have links from "categorylinks" table"""
    #     return cls.objects \
    #               .exclude(page_id__in=categorylinks.objects.filter()
    #                        .values_list('cl_from', flat=True)) \
    #               .filter(page_namespace=cls.NS_ARTICLE) \
    #               .filter(page_is_redirect=0)

    @property
    def unverified_revisions(self):
        return []

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Article)
def article_pre_save(instance, *args, **kwargs):
    # if instance.debug is None:
    #     instance.debug = {}

    # TODO: handle redirects when renaming
    instance.slug = slugify(unidecode(instance.title))


# quersyset.filter(pk=instance.pk).update(....)
@receiver(post_save, sender=Article)
def article_post_save(instance, *args, **kwargs):
    # TODO: Index in search engine
    pass

    # ERROR can be here about connection to ES
    # if instance.ok:
    # es = Elasticsearch()
    # es.index(
    #     index="articles",
    #     doc_type="article",
    #     id=instance.pk,
    #     body={
    #         "title": instance.title,
    #         "html": strip_tags(instance.html),
    #         # "timestamp": datetime.now()
    #         "changed_on": instance.changed_on,
    #         "ok": instance.ok,
    #     }
    # )

    # Only update PDF when title or content changed
    # it's POST_save
    # dirty = instance.get_dirty_fields()
    # if 'title' in dirty or 'rev' in dirty:
    # try:
    #     from .tasks import article_update_pdf
    #     article_update_pdf.delay(instance)
    # except:
    #     client.captureException()
