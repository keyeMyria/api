import core
from core.urls import urls_base
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from .sitemaps import RootSitemap
from .api.urls import urlpatterns as api_urls
from .views import (
    Index,
    FAQ,
    Contacts,
    Students,
    CourseView,
    PayView,
    Agreement,
    TestCallback,
)


courses_urls = ([
    path('<slug>', CourseView.as_view(), name="course"),
    # path(r'^$', include('core.urls', namespace='core')),
    # path(r'^articles/', include('articles.urls', namespace='articles')),
], 'courses')

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
    *core.urls.urlpatterns,
    path('accounts/', include('allauth.urls')),
    # path('accounts/vk/login/callback/', TestCallback.as_view(), name='cb'),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('articles/', include('articles.urls', namespace='articles')),
    path('api/', include(api_urls, namespace='api')),
    path('courses/', include(courses_urls, namespace='courses')),
]

urlpatterns += i18n_patterns(
    path('', Index.as_view(), name="index"),
    # path(r'^$', Index.as_view(), name="lazysignup_convert"),
    path('pay', PayView.as_view(), name='pay'),
    path('contacts', Contacts.as_view(), name='contacts'),
    path('students', Students.as_view(), name='students'),
    path('faq', FAQ.as_view(), name="faq"),
    path('agreement', Agreement.as_view(), name="agreement"),
    # path('login', Login.as_view(), name='login'),

    # This really needs to be here, not just in 'core' urls.py.
    # Because admin templates are getting reverse urls with "admin:..."
    # So if you wrap admin inside some app - reverse will throw an error
    # path('_/django/', admin.site.urls),

    prefix_default_language=False
)

# urlpatterns += [
#     path(r'^cas/', include('mama_cas.urls'))
# ]
