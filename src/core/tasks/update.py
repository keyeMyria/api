"""Tasks for updating this site."""
import re
import os
import json
import redis
from celery import shared_task
from celery import chain
from subprocess import call, Popen, PIPE
from django.conf import settings
from .. import now, apps


def updatelog(sha1, msg=None, clear=False):
    key = 'updatelog_'+sha1
    r = redis.StrictRedis(host=settings.SESSION_REDIS_HOST, port=6379, db=0)
    if clear:
        s = ""
        r.set(key, s, ex=3600*24*30)
    else:
        s = r.get(key)
        if s is None:
            s = ""
        else:
            s = s.decode()
    if msg is None:
        return s
    s += msg
    r.set(key, s, ex=3600*24*30)
    return s


# def supervisor(jobname, cmd):
@shared_task
def supervisor(*args):
    pass
    # return call(['sudo', 'supervisorctl', cmd, jobname])
    # return Popen(['sudo', 'supervisorctl', cmd, jobname])
    # kill -HUP $pid
    # {{repo}}/tmp/celery.pid
    # from django.conf import settings
    # Popen([
    #     'sudo',
    #     'kill',
    #     "-HUP",
    #     os.path.join(settings.GIT_PATH, "tmp", "celery.pid")
    # ])
    # return "ok"


@shared_task
def restart_celery(*args):
    pidfile = os.path.join(settings.GIT_PATH, "tmp", "celery.pid")
    pid = ''
    with open(pidfile) as f:
        pid = f.read().strip()
    Popen(['sudo', 'kill', "-HUP", pid])
    return "ok"


@shared_task
def build_css(sha1, *args):
    """Find scss files and compile them to css"""
    # find . -type f -name "*.scss" -not -name "_*" \
    # -not -path "./node_modules/*" -not -path "./static/*" -print \
    # | parallel --no-notice sass --cache-location /tmp/sass \
    # --style compressed {} {.}.css

    # find scss:
    # find all .scss files, but not starting with "_" symbol,
    # and not under /node_modules/, /static/ folders
    try:
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
        updatelog(sha1, "\nCompile CSS...\n{}\n".format(output))
    except Exception as e:
        updatelog(sha1, "\nERROR compiling CSS...\n{}\n".format(str(e)))
    return sha1


@shared_task
def migrate(sha1, *args):
    cmd = [
        settings.VEPYTHON,
        os.path.join(settings.GIT_PATH, 'src', 'manage.py'),
        'migrate'
    ]
    updatelog(sha1, "\nMigrate...\n")
    call(cmd)
    return sha1


@shared_task
def collect_static(sha1, *args):
    # tmp/ve/bin/python ./src/manage.py collectstatic --noinput
    # -i *.scss -i *.sass -i *.less -i *.coffee -i *.map -i *.md
    cmd = [
        settings.VEPYTHON,
        os.path.join(settings.GIT_PATH, "src", "manage.py"),
        'collectstatic', '--noinput',
        '-i', '*.scss', '-i', '*.sass', '-i', '*.less', '-i', '*.coffee',
        '-i', '*.map', '-i', '*.md'
    ]
    p = Popen(cmd, stdout=PIPE)
    output, err = p.communicate()
    updatelog(sha1, "\nCollect static...\n{}\n".format(output))
    return sha1

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
def get_project_at_commit(sha1):
    """Clone a repo and place it near current working project.

    If current project is in /var/www/prj, a new one will be in
    /var/www/ef49782e...4c09a305 for example.

    """
    updatelog(sha1, "\nCloning...\n")
    dst = os.path.join(
        os.path.dirname(settings.REPO_PATH),  # parent path of current project
        sha1                                  # use SHA1 as folder name
    )
    if os.path.isdir(dst):
        updatelog(
            sha1,
            "Path {} already exists. Skipping.\n".format(dst)
        )
        return sha1

    # git clone...
    cmd = [
        'git', 'clone', '--depth=1',
        'https://github.com/pashinin-com/pashinin.com.git',
        dst
    ]
    p = Popen(cmd, stdout=PIPE)
    output, err = p.communicate()
    updatelog(sha1, "{}\n{}\n".format(" ".join(cmd), output))
    return sha1


@shared_task
def project_update(sha1):
    """This task runs when Travis build is finished succesfully.

    Runs in core/hooks/views.py: Travis class
    """
    updatelog(sha1, clear=True)  # clear log in case we've already run this job
    chain(
        get_project_at_commit.s(sha1),
        build_css.s(),
        collect_static.s(),
        migrate.s(),
        # chain(
        #     supervisor.s("worker-"+settings.DOMAIN, "restart"),
        #     restart_celery.s()
        # ),
        update_finish.s()
    )()  # get() waits for all subtasks
    # supervisor.delay("worker-"+settings.DOMAIN, "restart")
    # restart_celery.delay()


@shared_task
def update_finish(sha1, *args):
    from core.models import SiteUpdate
    upd, created = SiteUpdate.objects.get_or_create(sha1=sha1)
    upd.log = updatelog(sha1)
    upd.finished = now()
    upd.save()
    return sha1


@shared_task
def render_jinja_file(filename, data, outdir=None):
    full = os.path.abspath(filename)
    d = os.path.dirname(full)
    base, ext = os.path.splitext(os.path.basename(full))
    output = os.path.join(d, base)
    if outdir is not None:
        output = os.path.join(outdir, base)

    input = open(full, 'r').read()
    from jinja2 import Environment
    with open(output, 'w') as f:
        f.write(Environment().from_string(input).render(**data))


@shared_task
def generate_settings():
    """Scans all apps and (re)generates settings.py files.

    It looks for 'settings.py.mustache' files and runs mustache command
    to render a file.

    """
    conf = os.path.join(settings.REPO_PATH, "configs", "tmp", "conf.py")
    data = json.load(open(conf, 'r'))
    for app, path in apps():
        templates = [os.path.join(path, f) for f in os.listdir(path)
                     if re.match(r'settings.*\.jinja', f)]
        for template in templates:
            print(template)
            render_jinja_file(template, data)
