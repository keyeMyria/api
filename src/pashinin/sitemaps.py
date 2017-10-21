from core import reverse, Sitemap


# example.org
class RootSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'
    # location = '/'
    protocol = 'https'
    # i18n = True

    def items(self):
        # return {'location': 'asd'}
        return [
            'index',
            'faq',
            'contacts',
        ]

    # https://testserver//pashinin.com/ - when "make test"
    # https://example.org//pashinin.com/ - when in browser
    def location(self, item):
        return reverse(item)
