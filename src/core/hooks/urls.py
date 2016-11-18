from django.conf.urls import url
from .views import *  # noqa

urlpatterns = [
    url(r'^github$', Github.as_view(), name="github"),
    url(r'^travis$', Travis.as_view(), name="travis"),
    url(r'^telegram$', Telegram.as_view(), name="telegram"),
]
