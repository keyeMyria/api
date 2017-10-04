import pytest
# import subprocess
import requests
import gzip
import itertools
# from tidylib import tidy_document
from subprocess import Popen, PIPE
from io import BytesIO
from core.tests import validate_process, validate_html
from bs4 import BeautifulSoup as Soup


# @pytest.mark.urls('pashinin.urls')
def test_sitemap_urls(admin_client):
    "Take all URLs from /sitemap.xml and check that HTML code is valid."
    r = admin_client.get('/sitemap.xml')
    soup = Soup(r.content, features="xml")
    # urls = soup.findAll('url')
    for loc in soup.findAll('loc'):
        url = loc.text
        path = url[url[10:].find('/')+10:]
        r = admin_client.get(url)
        assert r.status_code == 200


        # Validate
        res = validate_html(r.content, r['Content-Type'])
        validate_process(res, r.content)
        assert res == ''
