from django.contrib import sitemaps
from django.core.urlresolvers import reverse


# example.org
class RootSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = 'daily'
    location = '/'
    protocol = 'https'
    # i18n = True

    def items(self):
        return [
            'index',
            'faq',
            'contacts',
        ]

    def location(self, item):
        return reverse(item)
