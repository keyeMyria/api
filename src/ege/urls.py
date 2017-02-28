from django.contrib import admin
from django.conf.urls import url, include
from .views import (
    YearView,
    SubjectView,
    Index,
    ExamTaskView,
    TaskView,
    SubjectTheoryView,
    SubjectTasks
)
from core.views import Login


# /subj(/year)?/tasks/
tasks_patterns = [
    url(r'^$', SubjectTasks.as_view(), name="index"),
    url(r'^(?P<id>\d+)$', ExamTaskView.as_view(), name='task'),
]


# /subj(/year)?/
subject_patterns = [
    url(r'^$', SubjectView.as_view(), name="index"),
    url(r'^tasks/', include(tasks_patterns, namespace='tasks')),
    url(r'^theory$', SubjectTheoryView.as_view(), name='theory'),
    # url(r'^(?P<id>\d+)/(?P<slug>.+)$', TaskView.as_view(), name='task'),
]

# Main urls in "ege.example.org"
urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    # url(r'^task/(?P<id>\d+)/(?P<slug>.+)$', TaskView.as_view(), name='task'),

    # subjects by year
    url(r'^(?P<year>\d{4})/$', YearView.as_view(), name="year"),
    # url(r'^(?P<year>\d+)(/(?P<subj>\w+))?/$',
    #     SubjectView.as_view(), name="subject"),

    # by subject
    url(r'^(?P<subj>[a-z]([a-z]|\-)*)(/(?P<year>\d+))?/',
        include(subject_patterns, namespace='subject')),


    url(r'^login$', Login.as_view(), name='login'),
    url(r'^_/', include('core.urls', namespace='core')),
    url(r'^_/django/', include(admin.site.urls)),
]
