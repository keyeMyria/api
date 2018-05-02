import core
from core import admin
from core.urls import urls_base
from django.urls import path, include
# from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from .sitemaps import RootSitemap
from .views import (
    Baumanka,
    Kafedra,
    PeriodView,
    Practice,
)


sitemaps = {
    'static': RootSitemap,
}


# urlpatterns =
# urlpatterns = core.urls.urlpatterns
urlpatterns = [
    *core.urls.urlpatterns,
    # path('_/', include('core.urls', namespace='core')),
    # path('', include('core.urls', namespace='core')),
    # path('django/', admin.site.urls),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    path('',  Baumanka.as_view(), name="index"),
    # path('<faculty><int:kafedra>/', Kafedra.as_view(), name="kafedra"),

    # department
    path('<dpt_code>/', Kafedra.as_view(), name="kafedra"),
    # path('<dpt_code>/', include('baumanka.core.urls', namespace='dpt')),
    #

    # practice
    path('<dpt_code>/practice',
         Practice.as_view(), name="practice"),

    # sem
    # path('<faculty><int:kafedra>/sem<int:sem><path:path>',
    path('<dpt_code>/<period_code><path:path>',
         PeriodView.as_view(), name="sem"),
]
