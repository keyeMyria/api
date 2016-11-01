from django.conf.urls import url
from .views import *

urlpatterns = [
    # url(r'^upload$', Upload.as_view(), name="upload"),
    url(r'^(?P<sha1>.{40})$', File.as_view(), name="file"),
]
