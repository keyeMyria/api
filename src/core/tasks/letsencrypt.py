# import os
import celery
from celery import states
import logging
from celery import shared_task
from django.conf import settings
from subprocess import Popen
from core.install.apt import sh
log = logging.getLogger(__name__)


# @app.task(ignore_result=True)
@shared_task(bind=True)
def update_certs(self, *args):
    """Run it once in 2.5 months to update LetsEncrypt certificates.

    """
    if settings.DEBUG:
        msg = "Can't update LetsEncrypt certs while in DEBUG mode"
        log.debug(msg)
        # self.update_state(state=states.REVOKED)
        # raise celery.exceptions.Ignore()
        raise NotImplementedError(msg)

    cmd = ['sudo', 'certbot', 'renew', '--dry-run']
    sh(cmd)['code'] == 0
    p = Popen(['sudo', 'certbot', 'renew', '--dry-run'])
    output, err = p.communicate()
    # print(output, err)
    # log.debug(output)
    # raise ValueError(output, err)
    # pidfile = os.path.join(settings.GIT_PATH, "tmp", "celery.pid")
    # pid = ''
    # with open(pidfile) as f:
    #     pid = f.read().strip()
    return "ok"
