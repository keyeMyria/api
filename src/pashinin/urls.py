from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.template.loader import render_to_string
from django.http import HttpResponseNotFound
# from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from core.views import Login
from .views import (
    Index,
    FAQ,
    Contacts
)

# Error handlers
#
# https://docs.djangoproject.com/en/dev/ref/urls/#django.conf.urls.handler400
#
# def err404(request):
#     if request.method == 'GET':
#         return HttpResponseNotFound(render_to_string('404.html', locals()))
#     else:
#         return HttpResponseNotFound('404')


# def err500(request):
#     if request.method == 'GET':
#         return HttpResponseNotFound(render_to_string('500.html', locals()))
#     else:
#         return HttpResponseNotFound('500')


# handler404 = 'proj.urls.err404'
# handler500 = 'pashinin.urls.err500'
# handler404 = IndexView.as_view()

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    # url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
    #     name='django.contrib.sitemaps.views.sitemap'),
    url(r'^articles/', include('articles.urls', namespace='articles')),
    url(r'^baumanka/', include('baumanka.urls', namespace='baumanka')),
    url(r'^_/', include('core.urls', namespace='core')),
]

urlpatterns += i18n_patterns(
    url(r'^$', Index.as_view(), name="index"),
    url(r'^contacts$', Contacts.as_view(), name='contacts'),
    url(r'^faq$', FAQ.as_view(), name="faq"),
    url(r'^login$', Login.as_view(), name='login'),

    url(r'^_/django/', include(admin.site.urls)),
    prefix_default_language=False
)
