from django.contrib import admin
from django.conf.urls import url, include
from .views import *  # noqa

# ege.example.org
urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),  #
    # url(r'hooks/', include('core.hooks.urls', namespace='hooks')),
    # url(r'^nginx$', Nginx.as_view(), name='nginx'),
    # url(r'^updates$', Updates.as_view(), name='updates'),
    url(r'^(?P<subj>\w+)/$', SubjectView.as_view(), name="subject"),

    url(r'^_/', include('core.urls', namespace='core')),
    url(r'^_/django/', include(admin.site.urls)),
]
