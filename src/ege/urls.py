from django.contrib import admin
from django.conf.urls import url, include
from .views import (
    YearView,
    SubjectView,
    Index,
    ExamTaskView,
    # TaskView,
    SubjectTheoryView,
    SubjectTasks
)


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
    url(r'^(?P<year>\d+)$', SubjectView.as_view(), name="year"),
    # url(r'^(?P<id>\d+)/(?P<slug>.+)$', TaskView.as_view(), name='task'),
]

# Main urls in "ege.example.org"
urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    # url(r'^task/(?P<id>\d+)/(?P<slug>.+)$', TaskView.as_view(), name='task'),

    # /yyyy - all subjects by year
    url(r'^(?P<year>\d{4})$', YearView.as_view(), name="year"),
    # url(r'^(?P<year>\d+)(/(?P<subj>\w+))?/$',
    #     SubjectView.as_view(), name="subject"),

    # /subject[/yyyy]
    url(r'^(?P<subj>[a-z]([a-z]|\-)*)/',
        include(subject_patterns, namespace='subject')),


    url(r'^_/', include('core.urls', namespace='core')),
    url(r'^_/django/', include(admin.site.urls)),
]
