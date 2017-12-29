import os
# import sys
# import urllib
# import paramiko
from . import remote, systemd
from celery import shared_task
from core import get_git_root
# from django.conf import settings
import logging
log = logging.getLogger(__name__)


@shared_task
def install():
    """Install Stolon binaries in /usr/local/bin/

    stolonctl
    stolon-sentinel
    stolon-keeper

    """
    print('Installing Stolon...')

    hosts = (
        '10.254.239.1',  # server
        '10.254.239.2',  # desktop
        '10.254.239.3',  # student
    )

    for host in hosts:
        c = remote.create_connection(host)
        install_stolon_binaries(host, c=c)
        remote.mkdirs('/var/lib/stolon', host, c=c, owner='postgres')
        remote.mkdirs('/var/lib/stolon/postgres', host, c=c, owner='postgres')
        print(f'------{host}-------')
        # print(systemd.render_config('stolon-sentinel.jinja'))

        # sentinel systemd
        r = '/etc/systemd/system/stolon-sentinel.service'
        f = os.path.join(
            get_git_root(),
            'configs',
            'systemd-stolon-sentinel.jinja'
        )
        ftp = c.open_sftp()
        ftp.put(f, r)
        ftp.close()

        # keeper systemd
        f = '/etc/systemd/system/stolon-keeper.service'
        remote.write(f, systemd.render_config(
            'stolon-keeper.jinja',
            uid='postgres'+host.split('.')[-1],
            host=host,
        ), host, c=c)

        # proxy systemd
        r = '/etc/systemd/system/stolon-proxy.service'
        f = os.path.join(
            get_git_root(),
            'configs',
            'systemd-stolon-proxy.jinja'
        )
        ftp = c.open_sftp()
        ftp.put(f, r)
        ftp.close()


def install_stolon_binaries(host, c=None):
    """Download and install Stolon binaries.

    If there is no stolonctl - download and extract an archive

    """
    url = 'https://github.com/sorintlab/stolon/releases/download/' \
          'v0.7.0/stolon-v0.7.0-linux-amd64.tar.gz'
    basename = os.path.basename(url)
    basename_noext = 'stolon-v0.7.0-linux-amd64'
    filename = os.path.join('/tmp', basename)
    if c is None:
        c = remote.create_connection(host)

    if remote.file_exists('/usr/local/bin/stolonctl', host, c=c):
        print(f'Stolon is already installed on {host}')
    else:
        if remote.file_exists(filename, host, c=c):
            print(f'{filename} exists on {host}')
        else:
            print(f'Going to download {basename} on {host}...')
            filename = remote.download(url, host, c=c)

        if remote.isdir(basename_noext, host, c=c):
            print('extracted')
        else:
            res = remote.untar(filename, host=host, c=c)
            print(res['out'], res['err'])

        res = remote.get_output(
            f'cp {basename_noext}/bin/* /usr/local/bin/',
            host=host,
            c=c
        )
        print(res)
