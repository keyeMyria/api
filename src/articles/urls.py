from django.conf.urls import url
from .views import *  # noqa

urlpatterns = [
    url(r'^$', Articles.as_view(), name="index"),
    # url(r'^drafts$', DraftsView.as_view(), name="drafts"),
    # url(r'^tagged/(?P<title>.+)$', CategoryView.as_view(), name="tagged"),
    # url(r'^untagged$', UntaggedView.as_view(), name="untagged"),
    # url(r'^edit/(?P<id>\d+)$', ArticleEditView.as_view(), name="edit"),
    # url(r'^remove/(?P<title>.+)$', Remove.as_view(), name="remove"),
    # url(r'^writerev$', WriteRevision.as_view(), name="write"),
    # url(r'^write/(?P<id>\d+)$', WriteRevision.as_view(), name="write"),
    url(r'^(?P<id>\d+)/(?P<slug>.+)$', ArticleView.as_view(), name="article"),
]
