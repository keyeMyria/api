from django.conf.urls import include, url
from .views import (
    Celery,
    Nginx,
    Updates,
    Login,
    Logout
)

# These urls go under "core" namespace url: /_/
urlpatterns = [
    url(r'^celery$', Celery.as_view(), name='celery'),
    url(r'hooks/', include('core.hooks.urls', namespace='hooks')),
    url(r'files/', include('core.files.urls', namespace='files')),
    url(r'^nginx$', Nginx.as_view(), name='nginx'),
    url(r'^updates$', Updates.as_view(), name='updates'),
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^logout$', Logout.as_view(), name='logout'),
]
