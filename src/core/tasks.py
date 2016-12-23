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
from django.conf import settings


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
    Popen([
        'sudo',
        'kill',
        "-HUP",
        os.path.join(settings.GIT_PATH, "tmp", "celery.pid")
    ])
    return "ok"


@shared_task
def build_css():
    """Find scss files and compile them to css"""
    # find . -type f -name "*.scss" -not -name "_*" \
    # -not -path "./node_modules/*" -not -path "./static/*" -print \
    # | parallel --no-notice sass --cache-location /tmp/sass \
    # --style compressed {} {.}.css

    # find scss:
    # find all .scss files, but not starting with "_" symbol,
    # and not under /node_modules/, /static/ folders
    cmd1 = [
        "find", settings.GIT_PATH, "-type", "f", "-name", '"*.scss"',
        '-not', '-name', '"_*"', '-not', '-path', '"./node_modules/*"',
        '-not', '-path', '"./static/*"', '-print'
    ]
    # compile css
    cmd2 = [
        "parallel", "--no-notice", "sass", '--cache-location',
        '/tmp/sass', '--style', 'compressed', '{}', '{.}.css'
    ]
    p1 = Popen(cmd1, stdout=PIPE)
    p2 = Popen(cmd2, stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output, err = p2.communicate()
    return output


@shared_task
def collect_static():
    # tmp/ve/bin/python ./src/manage.py collectstatic --noinput
    # -i *.scss -i *.sass -i *.less -i *.coffee -i *.map -i *.md
    cmd = [
        settings.VEPYTHON,
        os.path.join(settings.GIT_PATH, "src", "manage.py"),
        'collectstatic', '--noinput',
        '-i', '*.scss', '-i', '*.sass', '-i', '*.less', '-i', '*.coffee',
        '-i', '*.map', '-i', '*.md'
    ]
    call(cmd)

# @task_postrun.connect()
# @task_postrun.connect(sender=restart_celery)
# def task_postrun(signal=None, sender=None, task_id=None, task=None,
#                  args=None, kwargs=None, retval=None, state=None):
#     # note that this hook runs even when there has been an exception
#     # thrown by the task
#     # print "post run {0} ".format(task)
#     from django.conf import settings
#     Popen([
#         'sudo',
#         'kill',
#         "-HUP",
#         os.path.join(settings.GIT_PATH, "tmp", "celery.pid")
#     ])


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

    # make css (as www-data)
    # make collectstatic
    # build_css.delay()
    # collect_static.delay()
    build_css.apply_async(
        link=collect_static.s()
    )
    # collect_static.delay()
    # res = add.apply_async((2, 2), link=mul.s(16))
    # res.get()
    # supervisor.delay("celery", "restart")
    restart_celery.delay()
