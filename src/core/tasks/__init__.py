import os
import pickle
import hashlib
import requests
import re
from celery import shared_task
from django.core.cache import cache
# from raven.contrib.django.raven_compat.models import client
# from celery import chain
# from subprocess import call, Popen, PIPE
# from celery.signals import task_postrun
# from datetime import datetime
# from django.conf import settings
from .update import *  # noqa


def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)


def load_cookies(filename):
    """Returns what? dict?"""
    with open(filename, 'rb') as f:
        return pickle.load(f)


url_get_version = 7


@shared_task
def get(url, charset='utf-8', force=False):
    """Get URL with GET method.

    Return a tuple: (str, {'r': <response object>})

    """
    # v = 7

    import lxml
    from lxml.cssselect import CSSSelector as S

    cookies = '/tmp/cookies.txt'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    key = "url.get_" + hashlib.sha1(url.encode('utf-8')).hexdigest()
    html = cache.get(key, version=url_get_version)
    if html is not None and not force:
        return html, {'cached': True}

    try:
        r = requests.get(
            url,
            cookies=load_cookies(cookies),
            headers=headers
        )
    except Exception:
        r = requests.get(url, headers=headers)

    save_cookies(r.cookies, cookies)
    if r.status_code == 200:
        html = r.text
        tree = lxml.html.fromstring(html)
        meta = S('meta[http-equiv="Content-Type"]')(tree)
        if meta:
            content = meta[0].get('content')
            m = re.search('charset=(.*)', content)
            charset = m.group(1)
            # print(etree.tostring(meta[0]), charset)
            if charset:
                try:
                    html = r.content.decode(charset)
                except Exception:
                    # client.captureException()
                    pass
        cache.set(key, html, 3600, version=url_get_version)
        return html, {'r': r}
    else:
        return r.text, {'r': r}


# @shared_task
# def Popen(cmd):
#     from subprocess import Popen
#     if isinstance(cmd, str):
#         cmd = cmd.split()
#     Popen(cmd)


@shared_task
def install_pkg(pkg_name):
    from subprocess import Popen
    import platform
    # import subprocess

    # check if we are root
    # if os.geteuid() != 0:
    #     raise ValueError("Need to be root to install packages")

    if 'Linux' == platform.system():
        # platform.linux_distribution() deprecated in 3.7

        # Arch
        pacman = '/usr/bin/pacman'
        if os.path.isfile(pacman):
            p = Popen(['sudo', '-S', pacman, '-S', '--noconfirm', pkg_name])
            p.communicate()
            p.wait()
            # sudo_prompt = p.communicate(sudo_password + '\n')[1]
        else:
            raise NotImplementedError(
                "don't know how to install packages in this Linux")

    elif 'Windows' == platform.system():
        raise NotImplementedError(
            "don't know how to install packages in Windows")
    else:
        raise NotImplementedError(
            "don't know how to install packages in Unknown")


def service_is_running(service):
    # systemctl is-active sshd
    from subprocess import Popen
    exit_code = Popen(['systemctl', '-q', 'is-active', service]).wait()
    return exit_code == 0


def configure_docker():
    import docker
    cli = docker.from_env()
    try:
        cli.images.get('ubuntu:17.04')
    except Exception:
        print('Getting Ubuntu image...')
        cli.images.pull('ubuntu:17.04')

    try:
        cli.images.get('postgres:latest')
    except Exception:
        print('Getting Postgres image...')
        cli.images.pull('postgres:latest')

    print(os.getcwd())
    cli.images.build(path='../docker/', tag='pashinin.com')
    # container = cli.containers.run('pashinin.com',
    #                                detach=True)

    print(cli.containers.list())
    print(cli.images.list())


def install(program):
    from shutil import which
    from subprocess import Popen
    if which(program) is not None:

        if program == 'docker':
            if service_is_running('docker'):
                print('Docker is running')
            else:
                print('starting Docker...')
                p = Popen(['sudo', '-S', 'systemctl', 'start', 'docker'])
                p.communicate()
                p.wait()

            # check docker images
            try:
                import docker
                docker.from_env()
            except Exception:
                print('Installing docker via pip')
                p = Popen(['sudo', 'pip', 'install', 'docker'])
                p.communicate()
                p.wait()

            # if permission denied - add user to "docker" group
            try:
                import docker
                client = docker.from_env()
                client.containers.list()
            except Exception as e:
                print(e)
                # gpasswd -a user docker
                import getpass
                p = Popen(['sudo', 'gpasswd', '-a', getpass.getuser(),
                           'docker'])
                p.communicate()
                p.wait()
                msg = """You were added to group "docker".
Please restart! Logout and login may not help!"""
                print('*'*len(msg))
                print(msg)
                print('*'*len(msg))
                raise ValueError("Restart!")

            configure_docker()

        return

    import platform

    pkgs = {
        'flake8': {
            'ubuntu': 'python-flake8',
            'arch': 'flake8',
        },
        'docker': {
            # 'ubuntu': 'python-flake8',
            'arch': 'docker',
        },
        'docker-compose': {
            # 'ubuntu': 'python-flake8',
            'arch': 'docker-compose',
        },
    }
    if program in pkgs:
        if 'Linux' == platform.system():
            # platform.linux_distribution() deprecated in 3.7

            # Arch
            if os.path.isfile('/usr/bin/pacman'):
                install_pkg(pkgs[program]['arch'])
            else:
                raise NotImplementedError(
                    "don't know how to install {} in this Linux"
                    .format(program))

        elif 'Windows' == platform.system():
            raise NotImplementedError(
                "don't know how to install packages in Windows")
        else:
            raise NotImplementedError(
                "don't know how to install packages in Unknown")
    else:
        raise ValueError("Don't know how to install {}".format(program))
