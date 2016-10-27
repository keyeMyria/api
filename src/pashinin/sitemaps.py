from django.contrib import sitemaps
from django.core.urlresolvers import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = 'daily'
    location = '/'
    protocol = 'https'
    # i18n = True

    def items(self):
        return [
            'baumanka:index'
        ]

    def location(self, item):
        return reverse(item)
