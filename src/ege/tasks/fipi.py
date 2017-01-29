"""Открытый банк заданий ЕГЭ.

Parsing using Celery tasks.

"""
import re
import os
import redis
from celery import shared_task
from celery import chain
import requests
import hashlib
from django.core.cache import cache
import lxml.html
from lxml.cssselect import CSSSelector as S
from ..models import Subject
from django.template.defaultfilters import slugify
from unidecode import unidecode
from edu import subject_slug
from raven.contrib.django.raven_compat.models import client


def get(url):
    """Just GETs an URL."""
    key = "url.get_" + hashlib.sha1(url.encode('utf-8')).hexdigest()
    html = cache.get(key)
    if html is not None:
        return html
    r = requests.get(url)
    if r.status_code == 200:
        cache.set(key, r.text, 3600)
        return r.text


@shared_task
def ege_subjects_and_urls(*args):
    """Scans a root URL http://www.fipi.ru/content/otkrytyy-bank-zadaniy-ege

    Returns a list of pairs [(title.lower().capitalize(), url), ...]

    Example:

    >>> subjects_and_urls()
    >>> [('русский язык', 'http://85.142.162.119/os11/xmodules/...'), ...]

    """
    try:
        url = "http://www.fipi.ru/content/otkrytyy-bank-zadaniy-ege"
        tree = lxml.html.fromstring(get(url))
        links = S('div.content table a[href^="http://85."]')(tree)
        res = [(" ".join(el.text_content().split()).lower().capitalize(),
                el.get('href'))
               for el in links]

        subjects = (title for title, url in res)
        create_subjects(*subjects)
        # TODO: message if len(res) <> 15  (15 now)
        return res
    except:
        client.captureException()
        return []


@shared_task
def create_subjects(*args):
    try:
        for title in args:
            subject, created = Subject.objects.get_or_create(
                name=title,
                slug=subject_slug.get(
                    title,
                    slugify(unidecode(title)))
            )
    except:
        client.captureException()
