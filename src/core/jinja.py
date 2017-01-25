from __future__ import absolute_import  # Python 2 only

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.utils.translation import gettext_lazy as _
from jinja2 import Environment
from datetime import datetime
now = datetime.now()


def djrender(value):
    from django.template import Template, Context
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
        'extensions': ['cacheops.jinja2.cache']
    })
    env = Environment(**options)
    env.globals.update(
        {
            'static': staticfiles_storage.url,
            'url': reverse,
            '_': _,
            'file': get_file,
            'css': css,
            'len': len,
            'now': datetime.now,
        },
    )
    env.filters['djrender'] = djrender
    return env
