from django_hosts import patterns, host
from django.conf import settings


host_patterns = patterns(
    '',
    host(r'baumanka', 'baumanka.urls', name='baumanka'),
    host(r'api', 'api.urls', name='api'),
    host(r'ege', 'ege.urls', name='ege'),
    host(r'oge', 'ege.urls', name='oge'),

    host(settings.DOMAIN, 'pashinin.urls', name='pashinin'),
    host('moskva', 'pashinin.urls', name='moskva'),
    host('spb', 'pashinin.urls', name='spb'),
)
