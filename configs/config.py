#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import argparse
import json

# This program adds some variables to a supplied config file.
output = '/tmp/conf.json'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Base config file (JSON)')
    args = parser.parse_args()

    data = {}
    with open(args.file) as f:
        data = json.load(f)

    data['vebin'] = os.path.dirname(sys.executable)
    data['repo'] = os.path.dirname(
        os.path.abspath(os.path.dirname(__file__)))
    if (sys.version_info >= (3, 5)):
        # print(sys.executable)
        pass
    else:
        # print('create ve')
        pass

    with open(output, 'w') as f:
        json.dump(data, f)

    print(output, end="")
