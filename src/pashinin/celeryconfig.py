#
# This file is a part of Django's settings.py. It is included withing
# it.
#
from celery.schedules import crontab
from datetime import timedelta
from django.conf import settings

# Register our serializer methods into kombu
from kombu.serialization import register
from core.json import my_dumps, my_loads
register('myjson', my_dumps, my_loads,
         content_type='application/json',
         content_encoding='utf-8')


# CELERY_RESULT_BACKEND = 'redis://'
# CELERY_RESULT_BACKEND = 'redis://{{redis_server}}:6379/0'
CELERY_RESULT_BACKEND = settings.BROKER_URL

# Tell celery to use your new serializer:
CELERY_ACCEPT_CONTENT = ['myjson']
# CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'myjson'
CELERY_RESULT_SERIALIZER = 'myjson'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

CELERYD_POOL_RESTARTS = True
CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_SENT_EVENT = True
EMAIL_HOST = "10.254.239.1"
CELERY_TIMEZONE = 'Europe/Moscow'


# If Sentry logging in Django/Celery stopped working use:
CELERYD_HIJACK_ROOT_LOGGER = False

# Options:

# "expires" - Either a int, describing the number of seconds, or a
# datetime object that describes the absolute time and date of when the
# task should expire. The task will not be executed after the expiration
# time.

CELERYBEAT_SCHEDULE = {
    # 'discover_open_ports': {
    #     'task': 'cms.ip.tasks.discover_open_ports',
    #     # hour=‘0,8-17/2’ (at midnight, and every two hours during
    #     # office hours).
    #     'schedule': crontab(minute='*/2'),
    #     # 'options': {"expires": 10.0}
    # },
    # 'get_new_gosts': {
    #     'task': 'gost.tasks.get_new_gosts',
    #     # hour=‘0,8-17/2’ (at midnight, and every two hours during
    #     # office hours).
    #     'schedule': crontab(hour='*/3', minute=0),
    #     # 'options': {"expires": 10.0}
    # },
    # 'debug_task': {
    #     'task': 'proj.celery.debug_task',
    #     # 'schedule': crontab(minute='*/10'),
    #     "schedule": timedelta(seconds=10),
    #     # 'args': (1, 2),
    #     # 'options': {"expires": 10.0}
    # },
    #'every-minute': {
    #    'task': 'proj.celery.debug_task',
    #    'schedule': crontab(minute='*/1'),
    #    #'args': (1, 2)
    #},
}
