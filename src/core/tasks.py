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


@shared_task
def supervisor(jobname, cmd):
    # return call(['sudo', 'supervisorctl', cmd, jobname])
    # return Popen(['sudo', 'supervisorctl', cmd, jobname])
    # kill -HUP $pid
    # {{repo}}/tmp/celery.pid
    from django.conf import settings
    return Popen([
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
    supervisor.delay("celery", "restart")
