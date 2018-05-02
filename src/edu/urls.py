import core
from core.urls import urls_base
from django.urls import path
from .views import (
    Tasks
)


# # /subj(/year)?/tasks/
# tasks_patterns = ([
#     path('', SubjectTasks.as_view(), name="index"),
#     path('<id>', ExamTaskView.as_view(), name='task'),
# ], 'tasks')


# # /subj(/year)?/
# subject_patterns = ([
#     path('', SubjectView.as_view(), name="index"),
#     path('tasks/', include(tasks_patterns, namespace='tasks')),
#     path('theory', SubjectTheoryView.as_view(), name='theory'),
#     path('<int:year>', SubjectView.as_view(), name="year"),
#     # path(r'^(?P<id>\d+)/(?P<slug>.+)$', TaskView.as_view(), name='task'),
# ], 'subject')

# Main urls in "tasks.example.org"
urlpatterns = [
    *core.urls.urlpatterns,
    path('', Tasks.as_view(), name='index'),
]
