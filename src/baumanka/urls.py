from django.urls import path, include
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
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    path('',  Baumanka.as_view(), name="index"),
    path('<faculty><int:kafedra>/', Kafedra.as_view(), name="kafedra"),
    path('<faculty><int:kafedra>/practice',
         Practice.as_view(), name="practice"),
    # path(r'^(?P<F>\w+?)(?P<K>\d+)/sem(?P<sem>\d+)/$',
    #  Sem.as_view(), name="sem"),
    path('<faculty><int:kafedra>/sem<int:sem><path:path>',
         Sem.as_view(), name="sem"),
    # path(r'^(?P<F>.+)(?P<id>\d+)/', include(faculty.urls,
    #                                        namespace='faculty')),
    path('_/', include('core.urls', namespace='core')),
]

urlpatterns += i18n_patterns(
    path('login', Login.as_view(), name='login'),

    path('_/django/', admin.site.urls),
    prefix_default_language=False
)
