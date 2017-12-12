from django.contrib import admin
from django.urls import path, include
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
tasks_patterns = ([
    path('', SubjectTasks.as_view(), name="index"),
    path('<id>', ExamTaskView.as_view(), name='task'),
], 'tasks')


# /subj(/year)?/
subject_patterns = ([
    path('', SubjectView.as_view(), name="index"),
    path('tasks/', include(tasks_patterns, namespace='tasks')),
    path('theory', SubjectTheoryView.as_view(), name='theory'),
    path('<int:year>', SubjectView.as_view(), name="year"),
    # path(r'^(?P<id>\d+)/(?P<slug>.+)$', TaskView.as_view(), name='task'),
], 'subject')

# Main urls in "ege.example.org"
urlpatterns = [
    path('', Index.as_view(), name='index'),

    # path(
    #     r'^task/(?P<id>\d+)/(?P<slug>.+)$',
    #     TaskView.as_view(),
    #     name='task'
    # ),

    # /yyyy - all subjects by year
    path('<int:year>', YearView.as_view(), name="year"),
    # path(r'^(?P<year>\d+)(/(?P<subj>\w+))?/$',
    #     SubjectView.as_view(), name="subject"),

    # /subject[/yyyy]
    path('<subj>/',
         include(subject_patterns, namespace='subject')),


    path('_/', include('core.urls', namespace='core')),
    path('_/django/', admin.site.urls),
]
