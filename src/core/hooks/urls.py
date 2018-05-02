from django.conf.urls import url
from .views import (
    Github,
    Telegram,
    Travis,
)

app_name = 'hooks'
urlpatterns = [
    url(r'^github$', Github.as_view(), name="github"),
    url(r'^travis$', Travis.as_view(), name="travis"),
    # url(r'^telegram/token$', Telegram.as_view(), name="telegram"),
    url(r'^telegram/(?P<token>.*)$', Telegram.as_view(), name="telegram"),
]
