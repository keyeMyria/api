# import re
# import os
# import redis
from celery import shared_task
from django.core.cache import cache
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
    with open(filename, 'rb') as f:
        return pickle.load(f)


@shared_task
def get(url, charset='utf-8'):
    """Just GETs an URL."""
    v = 7
    cookies = '/tmp/cookies.txt'

    key = "url.get_" + hashlib.sha1(url.encode('utf-8')).hexdigest()
    html = cache.get(key, version=v)
    if html is not None:
        return html

    try:
        r = requests.get(url, cookies=load_cookies(cookies))
    except:
        r = requests.get(url)

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
                except:
                    client.captureException()
        cache.set(key, html, 3600, version=v)
        return html
    else:
        return None
