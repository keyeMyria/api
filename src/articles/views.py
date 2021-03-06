# import traceback
from pashinin.views import Base
from .models import Article  # Revision, ArticleCategory
# from django.utils.translation import ugettext as _
# from django.core.urlresolvers import reverse
from core import reverse
# from raven.contrib.django.raven_compat.models import client
from braces import views
from django.http import Http404
import logging
log = logging.getLogger(__name__)


class ArticlesBase(
        views.LoginRequiredMixin,
        views.SuperuserRequiredMixin,
        Base
):
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c["menu"].current = 'articles'
        c['timeago'] = True
        c['momentjs'] = True
        return c


class ArticleView(ArticlesBase):
    template_name = "articles_article.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        # c["search"] = True
        c["hljs"] = True
        slug = self.kwargs.get('slug', '')
        id = int(self.kwargs.get('id', 0))
        # user = c["user"]

        # Get article
        article = None
        try:
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            raise Http404

        if not article.published and not c['user'].is_superuser:
            raise Http404

        # Redirect article if wrong slug used
        if article.slug != slug:
            c['redirect'] = reverse(
                "articles:article",
                kwargs={'id': id, 'slug': article.slug}
            )
            log.debug("redirect: ", c['redirect'])

        c["article"] = article
        # When 'pdf' parameter exists - download article in PDF format
        # if 'pdf' in self.request.GET:
        #     try:
        #         from files.sendfile import send_file
        #         fname = article.title.strip(".")
        #         r = send_file(self.request, article.pdf.filename,
        #                       in_browser=True,
        #                       outFilename=fname+".pdf")
        #         return r
        #     except:
        #         client.captureException()
        #         return HttpResponse("")

        # if user.is_superuser:
        #     drafts = Article.objects.filter(is_draft=True,
        #                            namespace=Article.NS_ARTICLE)
        return c


class Articles(ArticlesBase):
    template_name = "articles_articles.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['stats'] = {
            'count': Article.objects.count(),
            'drafts': Article.objects.filter(published=False).count(),
        }
        # import pytz
        # c['tz'] = pytz.timezone('Europe/Moscow')
        c["menu"].current = 'articles'
        # c["categories"] = ArticleCategory.objects.filter(
        #                 parent=None, lng_id=lng) \
        #                .exclude(article__category=None)
        # c["articles"] = Article.objects.filter(ok=True, lng_code=lng) \
        #       .order_by('title')
        c["articles"] = Article.objects.filter().order_by('added')
        # ctx["submenu"] = SubMenu({
        # 'url': reverse('articles'), 'title': _('Articles')},
        #  {'url': reverse('books'), 'title': _('Books')},
        #  parent={'url': reverse('articles'), 'title': _('Articles')})
        # m.parent = {'url': reverse('articles'), 'title': 'asd'}
        return c
