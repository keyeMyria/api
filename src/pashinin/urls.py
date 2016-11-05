from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.template.loader import render_to_string
from django.http import Http404, HttpResponse, HttpRequest, HttpResponseNotFound
from django.contrib.sitemaps.views import sitemap
from .views import *


def err404(request):
    if request.method == 'GET':
        return HttpResponseNotFound(render_to_string('404.html', locals()))
    else:
        return HttpResponseNotFound('404')


def err500(request):
    if request.method == 'GET':
        return HttpResponseNotFound(render_to_string('500.html', locals()))
    else:
        return HttpResponseNotFound('500')


# handler404 = 'proj.urls.err404'
# handler500 = 'pashinin.urls.err500'
# handler404 = IndexView.as_view()

from .sitemaps import StaticViewSitemap
sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = []
urlpatterns += [
#     url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
#         name='django.contrib.sitemaps.views.sitemap'),
    url(r'^baumanka/',  include('baumanka.urls', namespace='baumanka')),
    url(r'^_/files/', include('core.files.urls', namespace='files')),
]

urlpatterns += i18n_patterns(
    # url(r'^_/', include('cms.adm.urls', namespace='adm')),
    url(r'^_/django/', include(admin.site.urls)),
    # # url(r'^(?P<id>\d+)/(?P<slug>.+)$', ArticleView.as_view(), name="view"),
    # url(r'^articles/', include('cms.article.urls', namespace='articles')),
    prefix_default_language=False
)

# from repetitor import views
# urlpatterns += i18n_patterns(
#     # url(r'^repetitor/', include('repetitor.urls', namespace='repetitor')),
#     url(r'^contacts$', views.Contacts.as_view(), name='contacts'),
#     # url(r'^contacts$', views.IT.as_view(), name='contacts'),
#     # url(r'^exams$', views.Exams.as_view(), name='exams'),
#     # url(r'^enroll$', views.Contacts.as_view(), name='enroll'),
#     # url(r'^courses/', include('repetitor.courses.urls',
#     #                           namespace='courses')),
#     prefix_default_language=False
# )

# urlpatterns += [
#     url(r'^faq/', include('repetitor.faq.urls', namespace='faq')),
#     url(r'^students$', views.Students.as_view(), name='students'),
# ]

# Main page
urlpatterns += i18n_patterns(
    url(r'^$', Index.as_view(), name="index"),
    # url(r'^$', Index.as_view(), name="index"),
    prefix_default_language=False
)
