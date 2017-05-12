#!/usr/bin/env python
'''
#
# /etc/hosts: static lookup table for host names
#

#<ip-address>   <hostname.domain.org>   <hostname>
127.0.0.1       localhost.localdomain   localhost
::1             localhost.localdomain   localhost
127.0.0.1       desktop

# End of file
'''


from __future__ import print_function
import os
import sys
import argparse
import json
import re


tld = 'example.org'

add = [
    tld,
    'baumanka.'+tld,
    'ege.'+tld,
    'oge.'+tld,
]


hosts = {}
append = '\n'

data = ''

with open('/etc/hosts', 'r') as f:
    data = f.read()
    lines = [line for line in data.split('\n')
             if not line.startswith('#') and line]
    for line in lines:
        parts = re.findall(r"[\w'.:\-]+", line)
        try:
            ip, host, domain = parts
        except:
            ip, domain = parts
        # print(domain)
        if domain in hosts:
            hosts[domain] += [ip]
        else:
            hosts[domain] = [ip]

        if domain in add:
            add.remove(domain)


for host in add:
    append += '127.0.0.1 ' + host + '\n'

with open('/etc/hosts', 'w') as f:
    f.write(data+append)
