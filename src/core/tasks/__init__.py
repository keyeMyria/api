import pickle
import hashlib
import requests
import re
from celery import shared_task
from django.core.cache import cache
# from raven.contrib.django.raven_compat.models import client
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
    """Returns what? dict?"""
    with open(filename, 'rb') as f:
        return pickle.load(f)


url_get_version = 7


@shared_task
def get(url, charset='utf-8', force=False):
    """Get URL with GET method.

    Return a tuple: (str, {'r': <response object>})

    """
    # v = 7

    import lxml
    from lxml.cssselect import CSSSelector as S

    cookies = '/tmp/cookies.txt'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    key = "url.get_" + hashlib.sha1(url.encode('utf-8')).hexdigest()
    html = cache.get(key, version=url_get_version)
    if html is not None and not force:
        return html, {'cached': True}

    try:
        r = requests.get(
            url,
            cookies=load_cookies(cookies),
            headers=headers
        )
    except Exception:
        r = requests.get(url, headers=headers)

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
                except Exception:
                    # client.captureException()
                    pass
        cache.set(key, html, 3600, version=url_get_version)
        return html, {'r': r}
    else:
        return r.text, {'r': r}
