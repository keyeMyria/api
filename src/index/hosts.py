from django_hosts import patterns, host
from django.conf import settings


host_patterns = patterns(
    '',
    host(r'baumanka', 'baumanka.urls', name='baumanka'),
    host(r'api', 'api.urls', name='api'),
    host(r'ege', 'ege.urls', name='ege'),
    host(r'oge', 'ege.urls', name='oge'),

    # pashinin
    host(settings.DOMAIN, settings.ROOT_URLCONF, name=settings.APP),

    host(r'moskva', 'pashinin.urls', name='moskva'),
    host(r'spb', 'pashinin.urls', name='spb'),
    host(r'tasks', 'edu.urls', name='tasks'),
)
