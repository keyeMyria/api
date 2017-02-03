#!/usr/bin/env python
from __future__ import print_function
import os
import re
import argparse
import json

# Usage:
#
#  ./render.py template.jinja ...
#

config_file = '/tmp/conf.json'


def render(filename, data, outdir=None):
    full = os.path.abspath(filename)
    d = os.path.dirname(full)
    base, ext = os.path.splitext(os.path.basename(full))
    output = os.path.join(d, base)
    if outdir is not None:
        output = os.path.join(outdir, base)

    input = open(full, 'r').read()
    from jinja2 import Environment
    with open(output, 'w') as f:
        f.write(Environment().from_string(input).render(**data))


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help='Templates to render')
    args = parser.parse_args()

    current_dir = os.path.dirname(os.path.abspath(__file__))

    data = json.load(open(config_file, 'r'))

    if args.files:
        for filename in args.files:
            render(filename, data)
    else:
        outdir = os.path.join(current_dir, 'tmp')
        templates = [
            os.path.join(current_dir, f) for f in os.listdir(current_dir)
            if re.match('.*\.jinja', f)
        ]
        # print(templates)
        for template in templates:
            print(template)
            render(template, data, outdir=outdir)
