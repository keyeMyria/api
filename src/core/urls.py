from django.contrib import admin
from django.urls import include, path
from .views import (
    Celery,
    Nginx,
    Updates,
    Login,
    Logout,
    Postgres,
)

app_name = 'core'

# These urls go under "core" namespace url: /_/
urlpatterns = [
    path('celery', Celery.as_view(), name='celery'),
    path('hooks/', include('core.hooks.urls', namespace='hooks')),
    path('files/', include('core.files.urls', namespace='files')),
    path('django/', admin.site.urls),
    path('nginx', Nginx.as_view(), name='nginx'),
    path('postgres', Postgres.as_view(), name='postgres'),
    path('updates', Updates.as_view(), name='updates'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    # path('convert/', include('lazysignup.urls')),
]
