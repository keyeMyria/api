from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'hooks/', include('core.hooks.urls', namespace='hooks')),
]
