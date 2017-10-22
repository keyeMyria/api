#!/usr/bin/env python
from __future__ import print_function
import os
from os.path import dirname, abspath, isfile
import sys
import subprocess

repo_path = dirname(abspath(dirname(__file__)))

if __name__ == "__main__":
    # ERROR: virtualenv is not compatible with this system or executable
    # TODO: pip install --upgrade virtualenv

    if (
            sys.version_info >= (3, 6) and
            not sys.executable == "/usr/local/bin/python"
    ):
        print(sys.executable, end="")
        sys.exit(0)

    # path to virtualenv: /repo/tmp/ve
    ve = abspath(os.path.join(
        repo_path,
        "tmp",
        "ve"
    ))
    pythonbin = abspath(os.path.join(
        ve,
        "bin",
        "python"
    ))
    if isfile(pythonbin):
        print(pythonbin, end="")
        sys.exit(0)

    if os.path.isdir(ve):
        import shutil
        shutil.rmtree(ve)
        # virtualenv -p /usr/bin/python3 $(ve_path)
        #     	$(vecmd)
        # $(pip) install -r $(requirements)
    # ln -sf /var/www/xdev/src/cms $(ve_path)/lib/python3.5/site-packages/cms
    os.makedirs(ve)

    # create ve
    p = subprocess.Popen(
        ["virtualenv", "-p", "/usr/bin/python3.6", ve],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate()
    print(pythonbin, end="")
