from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from .sitemaps import RootSitemap
from .api.urls import urlpatterns as api_urls
from .views import (
    Index,
    FAQ,
    Contacts,
    Students,
    CourseView
)


courses_urls = [
    url(r'^(?P<slug>.+)$', CourseView.as_view(), name="course"),
    # url(r'^$', include('core.urls', namespace='core')),
    # url(r'^articles/', include('articles.urls', namespace='articles')),
]

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
    'static': RootSitemap,
}

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^articles/', include('articles.urls', namespace='articles')),
    url(r'^api/', include(api_urls, namespace='api')),
    url(r'^courses/', include(courses_urls, namespace='courses')),
    # url(r'^baumanka/', include('baumanka.urls', namespace='baumanka')),
    url(r'^_/', include('core.urls', namespace='core')),
]

urlpatterns += i18n_patterns(
    url(r'^$', Index.as_view(), name="index"),
    # url(r'^$', Index.as_view(), name="lazysignup_convert"),
    url(r'^contacts$', Contacts.as_view(), name='contacts'),
    url(r'^students$', Students.as_view(), name='students'),
    url(r'^faq$', FAQ.as_view(), name="faq"),
    # url(r'^login$', Login.as_view(), name='login'),

    # url(r'^_/django/', include(admin.site.urls)),
    prefix_default_language=False
)

# urlpatterns += [
#     url(r'^cas/', include('mama_cas.urls'))
# ]
