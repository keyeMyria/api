from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^github$', Github.as_view(), name="github"),
]
