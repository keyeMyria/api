from django.contrib import admin
from django.conf.urls import url, include
from .views import YearView, SubjectView, Index

# ege.example.org
urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^(?P<year>\d{4})/$', YearView.as_view(), name="year"),
    # url(r'^(?P<year>\d+)(/(?P<subj>\w+))?/$',
    #     SubjectView.as_view(), name="subject"),
    url(r'^(?P<subj>[a-z]([a-z]|\-)*)/$',
        SubjectView.as_view(), name="subject"),


    url(r'^_/', include('core.urls', namespace='core')),
    url(r'^_/django/', include(admin.site.urls)),
]
