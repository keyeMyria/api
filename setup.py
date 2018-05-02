#!/usr/bin/env python3
# -*- mode: python -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import print_function
import os
import sys
import subprocess
from subprocess import Popen

try:
    import argcomplete  # noqa
    ARGCOMPLETE = True
except ImportError:
    ARGCOMPLETE = False
    print('Install argcomplete with:')
    print('    sudo -H pip2 install argcomplete')
    # subprocess.Popen('sudo -H pip2 install argcomplete'.split())
    print('Then run:')
    print('    sudo activate-global-python-argcomplete')


def run(cmd):
    process = subprocess.Popen(
        cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = process.communicate()
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
        stderr = Popen(
            'docker-compose up -d db django vnu celery'.split(),
            env=my_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate()[1].decode('utf-8').strip()
        if 'Couldn\'t connect to Docker daemon' in stderr and \
           kwargs.get('start', True):
            print('Docker is not started?')
            # Popen('sudo service docker start'.split()).communicate()
            # run('sudo service docker start')
            print('Start Docker with: sudo service docker start')
            sys.exit(0)
            # print('    ')
            # start_containers(**{**kwargs, 'start': False})
    except FileNotFoundError:
        print('No docker-compose? Run:')
        print('sudo apt -y install docker-compose')
        sys.exit(0)
        # print('**********************************************************')
        # print('LOG OUT AND THEN LOG IN. Otherwise Docker can have errors!')
        # print('**********************************************************')
        # start_containers(install=False)
        # start_containers(**{**kwargs, 'install': False})


def deploy():
    pass


print('Starting Docker images...')
start_containers()
