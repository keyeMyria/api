from django.conf.urls import include, url
from .views import *  # noqa

# These urls go under "core" namespace url: /_/
urlpatterns = [
    # url(r'^celery$', Celery.as_view(), name='celery'),
    # url(r'hooks/', include('core.hooks.urls', namespace='hooks')),
    # url(r'^nginx$', Nginx.as_view(), name='nginx'),
    # url(r'^updates$', Updates.as_view(), name='updates'),
]
