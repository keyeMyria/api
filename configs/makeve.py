#!/usr/bin/env python
"""
If in Travis build - return python executable path.
Ex.:

Creates Python environment in "tmp/ve" path or returns .
"""

from __future__ import print_function
import os
from os.path import dirname, abspath, isfile
import sys
import subprocess

repo_path = dirname(abspath(dirname(__file__)))

if __name__ == "__main__":
    # ERROR: virtualenv is not compatible with this system or executable
    # TODO: pip install --upgrade virtualenv

    # Travis
    if os.getenv('TRAVIS'):
        print(sys.executable, end="")
        sys.exit(0)

    # if (
    #         sys.version_info >= (3, 6) and
    #         not sys.executable == "/usr/local/bin/python"
    # ):
    #     print(sys.executable, end="")
    #     sys.exit(0)

    # path of our virtualenv - repo/tmp/ve
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

    # If python executable exists - return full path to it
    if isfile(pythonbin):
        print(pythonbin, end="")
        sys.exit(0)

    # Else - create a virtualenv:
    # remove ve first
    if os.path.isdir(ve):
        import shutil
        shutil.rmtree(ve)

    # and create a new one
    os.makedirs(ve)

    # create ve
    p = subprocess.Popen(
        ["virtualenv", "-p", "/usr/bin/python3.6", ve],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate()
    print(pythonbin, end="")
