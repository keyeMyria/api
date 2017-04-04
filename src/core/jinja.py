from __future__ import absolute_import  # Python 2 only

from django.contrib.staticfiles.storage import staticfiles_storage
# from django.core.urlresolvers import reverse
# from django_hosts.resolvers import reverse
from . import reverse
from django.utils.translation import gettext_lazy as _
from jinja2 import Environment
from datetime import datetime
from jinja2 import nodes
from jinja2.ext import Extension
import re
from django.utils.formats import date_format

now = datetime.now()


class SpacelessExtension(Extension):
    """Removes whitespace between HTML tags at compile time, including tab
    and newline characters.  It does not remove whitespace between
    jinja2 tags or variables. Neither does it remove whitespace between
    tags and their text content.  Adapted from coffin:
    https://github.com/coffin/coffin/blob/master/coffin/template/defaulttags.py

    """

    tags = set(['spaceless'])

    def parse(self, parser):
        # lineno = parser.stream.next().lineno
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(['name:endspaceless'], drop_needle=True)
        return nodes.CallBlock(
            self.call_method('_strip_spaces', [], [], None, None),
            [], [], body,
        ).set_lineno(lineno)

    def _strip_spaces(self, caller=None):
        return re.sub(r'>\s+<', '><', caller().strip())


def djrender(value):
    # from django.template import Template, Context
    # from cms.core.jinja import environment
    # t = Template(value)
    # c = Context({
    #     # "my_name": "Adrian"
    # })
    # t.render(c)
    return environment().from_string(value).render()


def get_file(hash):
    return reverse('core:files:file', kwargs={'sha1': hash})


def css(f):
    return '''<link rel="preload" href="{0}" as="style" onload="this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{0}"></noscript>'''.format(f)


def environment(**options):
    # env = Environment(**options)
    # env = Environment(trim_blocks=False, **options)
    options.update({
        'trim_blocks': True,
        'extensions': [
            'cacheops.jinja2.cache',
            SpacelessExtension,
        ]
    })
    env = Environment(**options)
    env.globals.update(
        {
            'static': staticfiles_storage.url,
            'url': reverse,
            '_': _,
            'file': get_file,
            'round': round,
            'css': css,
            'min': min,
            'len': len,
            'date_format': date_format,
            'now': datetime.now,
        },
    )
    env.filters['djrender'] = djrender

    # Timezone
    from django.utils.timezone import template_localtime
    env.filters.update({
        'localtime': template_localtime,
    })
    env.globals.update({
        'localtime': template_localtime,
    })
    return env
