from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from .sitemaps import RootSitemap
from core.views import Login
from .views import (
    Baumanka,
    Kafedra,
    Sem,
    Practice,
)


sitemaps = {
    'static': RootSitemap,
}

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    url(r'^$',  Baumanka.as_view(), name="index"),
    url(r'^(?P<F>\w+?)(?P<K>\d+)/$', Kafedra.as_view(), name="kafedra"),
    url(r'^(?P<F>\w+?)(?P<K>\d+)/practice$',
        Practice.as_view(), name="practice"),
    # url(r'^(?P<F>\w+?)(?P<K>\d+)/sem(?P<sem>\d+)/$',
    #  Sem.as_view(), name="sem"),
    url(r'^(?P<F>\w+?)(?P<K>\d+)/sem(?P<sem>\d+)/(?:(?P<path>.*)/?)?$',
        Sem.as_view(), name="sem"),
    # url(r'^(?P<F>.+)(?P<id>\d+)/', include(faculty.urls,
    #                                        namespace='faculty')),
    url(r'^_/', include('core.urls', namespace='core')),
]

urlpatterns += i18n_patterns(
    url(r'^login$', Login.as_view(), name='login'),

    url(r'^_/django/', include(admin.site.urls)),
    prefix_default_language=False
)
