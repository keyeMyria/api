#
# This file is a part of Django's settings.py. It is included withing
# it.
#
# from celery.schedules import crontab
# from datetime import timedelta
from django.conf import settings

# Register our serializer methods into kombu
# from kombu.serialization import register
# from core.json import my_dumps, my_loads
# register('myjson', my_dumps, my_loads,
#          content_type='application/json',
#          content_encoding='utf-8')


# CELERY_RESULT_BACKEND = 'redis://'
# CELERY_RESULT_BACKEND = 'redis://{{redis_server}}:6379/0'
CELERY_RESULT_BACKEND = settings.BROKER_URL

# Add a one-minute timeout to all Celery tasks.
CELERYD_TASK_SOFT_TIME_LIMIT = 60

# Tell celery to use your new serializer:
# CELERY_ACCEPT_CONTENT = ['myjson']
# CELERY_TASK_SERIALIZER = 'myjson'
# CELERY_RESULT_SERIALIZER = 'myjson'

# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

CELERYD_POOL_RESTARTS = True
CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_SENT_EVENT = True
EMAIL_HOST = "10.254.239.1"


# Problems if have TZ = TZ from Django project settings file
# 1. https://github.com/celery/celery/issues/4184
# 2. https://github.com/celery/celery/issues/4177
# 3. https://github.com/celery/celery/issues/4169
# CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True


# Please do not touch (and change) my logger, Celery!
# If Sentry logging in Django/Celery stopped working use:
CELERYD_HIJACK_ROOT_LOGGER = False
