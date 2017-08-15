#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import argparse
import json

# Usage:
#
#  ./config.py secret-example.json secret.json ...
#
# Description:
#
# This program scans all JSON files in order you give them and writes
# final JSON settings to "output" variable, default: /tmp/conf.json
#

output = 'tmp/conf.json'
repo_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
pythonbin = os.path.abspath(os.path.join(
    repo_path,
    "tmp",
    "ve",
    "bin",
    "python"))

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--param', default=None,
                        help="Extracts a value for a param")
    parser.add_argument('files', nargs='*', help='JSON files with settings')
    args = parser.parse_args()

    # Read all settings to "data" var
    data = {}
    for filename in args.files:
        try:
            with open(filename) as f:
                data.update(json.load(f))
        except IOError:
            pass

    # Make changes if we are in travis-ci.org build
    if os.getenv('TRAVIS', '') == 'true':
        data["redis_server"] = "127.0.0.1"
        data["dbhost"] = "127.0.0.1"

    # Put some additional variables
    data['out'] = output
    data['repo'] = repo_path
    data['wwwdata'] = 'travis' if os.getenv('TRAVIS') else 'www-data'

    if (sys.version_info >= (3, 5)):
        data['vebin'] = os.path.dirname(sys.executable)
    else:
        data['vebin'] = os.path.dirname(pythonbin)

    # if asked for 1 param - return it and exit
    if args.param:
        try:
            print(data[args.param], end="")
        except:
            pass
        finally:
            sys.exit(0)

    with open(output, 'w') as f:
        json.dump(data, f)

    print(output, end="")
