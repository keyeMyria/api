from django.conf.urls import url
from .views import (
    Files,
    Upload,
    File,
)

# In pashinin/urls.py
#
# /_/file/
urlpatterns = [
    url(r'^$', Files.as_view(), name="index"),
    url(r'^upload$', Upload.as_view(), name="upload"),
    url(r'^(?P<sha1>.{40})$', File.as_view(), name="file"),
]
