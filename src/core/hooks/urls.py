from django.conf.urls import url
from .views import (
    Github,
    Telegram,
    Travis,
)

urlpatterns = [
    url(r'^github$', Github.as_view(), name="github"),
    url(r'^travis/(?P<secret>.*)$', Travis.as_view(), name="travis"),
    url(r'^telegram/(?P<token>.*)$', Telegram.as_view(), name="telegram"),
]
