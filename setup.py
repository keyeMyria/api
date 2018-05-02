#!/usr/bin/env python3
# -*- mode: python -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import print_function
import subprocess
import os
from subprocess import Popen

try:
    import argcomplete  # noqa
    ARGCOMPLETE = True
except ImportError:
    ARGCOMPLETE = False
    subprocess.Popen('sudo -H pip2 install argcomplete'.split())
    print('sudo activate-global-python-argcomplete')


def run(cmd, **kwargs):
    p = subprocess.Popen(
        cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate()
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def docker_ps():
    for container in run('docker ps')[0].split('\n')[1:]:
        data = container.split()
        yield {
            'id': data[0],
            'name': data[-1],
        }

def start_containers(**kwargs):
    my_env = os.environ.copy()
    my_env["UID"] = str(os.getuid())
    try:
        Popen(
            'docker-compose2 up -d db django vnu celery'.split(),
            env=my_env
        ).communicate()
    except FileNotFoundError:
        print('No docker-compose?', flush=True)
        if kwargs.get('install', True):
            print('Installing Docker...', flush=True)
            Popen('sudo apt install docker-compose'.split()).communicate()
            print('docker-compose installed!')
            start_containers(install=False)
        else:
            raise


def deploy():
    pass


print('Checking running images...')
start_containers()
