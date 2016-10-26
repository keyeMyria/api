# from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# To call a task from a command line:
#  celery call proj.celery.debug_task

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pashinin.settings')
app = Celery('pashinin')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    # Request: <Context: {'id': '7655cbe0-c9b5-4bb6-941c-5bec8e37169e',
    # 'task': 'proj.celery.debug_task', 'errbacks': None, 'group': None,
    # 'called_directly': False, 'delivery_info': {'redelivered': False,
    # 'exchange': 'celery', 'routing_key': 'celery', 'priority': None},
    # 'eta': None, 'hostname': 'celery@xdev', 'headers': {}, 'reply_to':
    # '5b59109e-f2e7-3e99-b089-244e98828311', 'utc': True,
    # 'correlation_id': '7655cbe0-c9b5-4bb6-941c-5bec8e37169e', 'args':
    # [], 'chord': None, 'taskset': None, 'is_eager': False, 'expires':
    # None, 'timelimit': [None, None], 'retries': 0, '_protected': 1,
    # 'callbacks': None, 'kwargs': {}}> [2014-09-04 21:40:10,001:
    # INFO/MainProcess] Task
    # proj.celery.debug_task[7655cbe0-c9b5-4bb6-941c-5bec8e37169e]
    # succeeded in 0.05006996900192462s: None
