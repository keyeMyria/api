from core import reverse, Sitemap


# baumanka.example.org
class RootSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'
    # location = '/'
    protocol = 'https'
    # i18n = True

    def _items(self):
        yield '/'
        for F in ('IU', ):
            for K in (2, ):
                yield (F, K, None)
                for sem in range(1, 12+1):
                    yield (F, K, sem)

    def items(self):
        return [item for item in self._items()]

    def location(self, item):
        if item == '/':
            return reverse('index', host='baumanka')

        F, K, sem = item
        if sem is None:
            return reverse('kafedra', kwargs={
                'F': F,
                'K': K,
            }, host='baumanka')
        else:
            return reverse('sem', kwargs={
                'F': F,
                'K': K,
                'sem': sem,
                'path': ''
            }, host='baumanka')
