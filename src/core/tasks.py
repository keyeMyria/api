# import re
# import time
import os
from celery import shared_task
# from raven.contrib.django.raven_compat.models import client
# from datetime import timedelta
# from six.moves.urllib.parse import urljoin
# from celery import chain
# import string
# from celery import group, chord
# from .models import *
from django.core.mail import send_mail
from subprocess import call, Popen, PIPE
from celery.signals import task_postrun


@shared_task
def supervisor(jobname, cmd):
    # return call(['sudo', 'supervisorctl', cmd, jobname])
    # return Popen(['sudo', 'supervisorctl', cmd, jobname])
    # kill -HUP $pid
    # {{repo}}/tmp/celery.pid
    from django.conf import settings
    Popen([
        'sudo',
        'kill',
        "-HUP",
        os.path.join(settings.GIT_PATH, "tmp", "celery.pid")
    ])
    return "ok"


@shared_task
def restart_celery():
    return


# @task_postrun.connect()
@task_postrun.connect(sender=restart_celery)
def task_postrun(signal=None, sender=None, task_id=None, task=None,
                 args=None, kwargs=None, retval=None, state=None):
    # note that this hook runs even when there has been an exception
    # thrown by the task
    # print "post run {0} ".format(task)
    from django.conf import settings
    Popen([
        'sudo',
        'kill',
        "-HUP",
        os.path.join(settings.GIT_PATH, "tmp", "celery.pid")
    ])


@shared_task
def project_update(commit_sha1):
    # restart supervisor jobs
    body = "test"
    send_mail(
        commit_sha1,
        body,
        "update robot <ROBOT@pashinin.com>",
        ["sergey@pashinin.com"]
    )
    # supervisor.delay("celery", "restart")
    restart_celery.delay()
