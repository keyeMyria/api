from django.conf.urls import include, url
from .views import *  # noqa

# /_/
urlpatterns = [
    url(r'^celery$', Celery.as_view(), name='celery'),
    url(r'hooks/', include('core.hooks.urls', namespace='hooks')),
]
