from django.conf.urls import include, url
from .views import *  # noqa

urlpatterns = [
    url(r'hooks/', include('core.hooks.urls', namespace='hooks')),
]
