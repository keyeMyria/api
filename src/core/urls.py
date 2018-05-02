# from . import admin
from django.contrib import admin
from django.urls import include, path
from .views import (
    Celery,
    Cluster,
    Nginx,
    Updates,
    Login,
    Logout,
    Postgres,
    Profile,
)

# app_name = 'core'

# These urls go under "core" namespace url: /_/
urlpatterns = [
    path('celery', Celery.as_view(), name='celery'),
    path('hooks/', include('core.hooks.urls', namespace='hooks')),
    path('files/', include('core.files.urls', namespace='files')),
    # path('django/', admin.site.urls, name="core:admin"),
    path('admin/', admin.site.urls),
    # path('django/', include(
    #     'django.contrib.admin.urls',
    #     namespace='files')
    # ),
    path('cluster', Cluster.as_view(), name='cluster'),
    path('nginx', Nginx.as_view(), name='nginx'),
    path('postgres', Postgres.as_view(), name='postgres'),
    path('updates', Updates.as_view(), name='updates'),
    path('profile', Profile.as_view(), name='profile'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    # path('convert/', include('lazysignup.urls')),
]


urls_base = [
    # path('_/', include('core.urls', namespace='core')),
    path('_/', include((urlpatterns, 'core'), namespace='core')),
    # path(
    #     'sitemap.xml',
    #     sitemap,
    #     {'sitemaps': sitemaps},
    #     name='django.contrib.sitemaps.views.sitemap'
    # ),
    # path('api/', include(api_urls, namespace='api')),
]

# urlpatterns += i18n_patterns(
#     path('login', Login.as_view(), name='login'),
#     path('_/django/', admin.site.urls),
#     prefix_default_language=False
# )
