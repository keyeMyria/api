#!/usr/bin/env python3
# -*- mode: python -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import print_function
import os
import sys
import subprocess
from subprocess import Popen
from setuptools import setup

try:
    import argcomplete  # noqa
    ARGCOMPLETE = True
except ImportError:
    ARGCOMPLETE = False
    # FIXME: apt install python-pip3
    print('Install argcomplete with:')
    print('    sudo -H pip3 install argcomplete')
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
        process = Popen(
            # 'docker-compose up -d db django vnu celery'.split(),
            'docker-compose run --service-ports django '
            'python manage.py runserver 0.0.0.0:8000'.split(),
            env=my_env,
            # stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stderr = process.communicate()[1].decode('utf-8').strip()
        rc = process.returncode
        if 'Couldn\'t connect to Docker daemon' in stderr and \
           kwargs.get('start', True):
            print('Docker is not started?')
            # Popen('sudo service docker start'.split()).communicate()
            # run('sudo service docker start')
            print('Start Docker with: sudo service docker start')
            print('And add yourself to Docker group!!!')
            print('    sudo usermod -aG docker ${USER}')
            print('The error was:')
            print(stderr)
            sys.exit(0)
            # print('    ')
            # start_containers(**{**kwargs, 'start': False})
        elif rc != 0:
            print(stderr)
    except FileNotFoundError:
        print('No docker-compose? Run:')
        print('sudo apt -y install docker-compose')
        sys.exit(0)
        # FIXME: asd
        # print('**********************************************************')
        # print('LOG OUT AND THEN LOG IN. Otherwise Docker can have errors!')
        # print('**********************************************************')
        # start_containers(install=False)
        # start_containers(**{**kwargs, 'install': False})


def deploy():
    pass


print('Starting Docker images...')
# start_containers()


setup(
    name='pashinin',
    # version=version,
    description='My Django API',
    author='Sergey Pashinin',
    author_email='sergey@pashinin.com',
    url='https://github.com/pashinin-com/api',
    # setup_requires=['milksnake'],
    # install_requires=['milksnake'],
    # milksnake_tasks=[
    #     build_native
    # ],
    requires=[],
    packages=[  # directories to include
        # 'rparser'
    ],
    # distclass=RustDistribution,
    tests_require=['nose'],
    test_suite='nose.collector',
    cmdclass={
        # 'build_rust': build_rust_cmdclass(
        #     # [('.', 'rparser')],
        #     [('.', '.')],
        #     extra_cargo_args=[
        #         '--features', 'py3',
        #     ] if PY3 else
        #     [
        #         "--features", 'py2',
        #         '--no-default-features'
        #     ]
        # ),
        # 'install_lib': build_install_lib_cmdclass(),
        # 'test': PyTest,
    },

    zip_safe=False,

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=(
        # Development Status :: 1 - Planning
        # Development Status :: 2 - Pre-Alpha
        # Development Status :: 3 - Alpha
        # Development Status :: 4 - Beta
        # Development Status :: 5 - Production/Stable
        # Development Status :: 6 - Mature
        # Development Status :: 7 - Inactive
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ),
    platforms=["Windows", "Linux", "Mac OS-X"],
    # platforms='any',
)
