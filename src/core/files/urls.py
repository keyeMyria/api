from django.conf.urls import url
from .views import (
    DownloadCore,
    Files,
    Upload,
    FileView,
)

# In pashinin/urls.py
#
# /_/file/
urlpatterns = [
    url(r'^$', Files.as_view(), name="index"),
    url(r'^upload$', Upload.as_view(), name="upload"),
    url(r'^download_core$', DownloadCore.as_view(), name="download_core"),
    url(r'^(?P<sha1>.{40})$', FileView.as_view(), name="file"),
]
