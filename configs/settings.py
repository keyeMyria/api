# -*- mode: python -*-
import os
import sys
from os.path import dirname, abspath, basename
from cms.core import underDjangoDebugServer


dds = underDjangoDebugServer()

VAGRANT = True
testing = 'test' in sys.argv or '--reuse-db' in sys.argv
DEBUG = testing or VAGRANT
DEBUG = True

SETTINGS_PATH = dirname(abspath(__file__))
SITE_PATH = dirname(abspath(__file__))
GIT_PATH = dirname(dirname(SETTINGS_PATH))
GIT_PATH = '/var/www/pashinin.com'

MODULE = basename(dirname(SITE_PATH))

# If you have a mail server - error messages are posted to admins
ADMINS = (
    ('Admin', 'sergey@pashinin.com'),
)
MANAGERS = ADMINS
SERVER_EMAIL = 'Error <robot@pashinin.com>'      # "From" field

# Databases
# sudo apt-get install pgbouncer
# vim /etc/pgbouncer/pgbouncer.ini
# [databases]
# * = host=127.0.0.1 port=5433
# /etc/pgbouncer/userlist.txt
# "user" "password"
DB_ENGINE_MYSQL = 'django.db.backends.mysql'
DB_ENGINE_POSTGRE = 'django.db.backends.postgresql_psycopg2'
DATABASE_ENGINE = DB_ENGINE_POSTGRE
is_sqlite = (DATABASE_ENGINE == 'django.db.backends.sqlite3')
DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        # 'NAME': "test.db" if is_sqlite else "db",
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        # 'HOST': "127.0.0.1",
        'PORT': '',
        # 'PORT': '6432',
    },
    'sentry': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': 'sentry',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
ugettext = lambda s: s
LANGUAGES = (
    ('en-us', 'English'),
    ('en', 'English'),
    ('ru', 'Russian'),
)

LOCALE_PATHS = (
    # 'locale',
    os.path.join(SETTINGS_PATH, 'locale'),     # replace SITE_PATH with yours
)

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False       # needs to be False for DATETIME_FORMAT to work

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
DATETIME_FORMAT = "Y-m-d H:i:sO"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(GIT_PATH, 'files', 'uploads/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/_sp/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(GIT_PATH, "static")
FILES_ROOT = os.path.join(GIT_PATH, "files")


# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/_s/'

# Additional locations of static files
STATICFILES_DIRS = (
    # os.path.join(SETTINGS_PATH, "static"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cms.core.auth.AuthenticationMiddleware',  # by email
    'django.contrib.messages.middleware.MessageMiddleware',

    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django_pdb.middleware.PdbMiddleware',
)

ROOT_URLCONF = 'pashinin.urls'

# Python dotted path to the WSGI application used by Django's runserver.
# Default: None
# WSGI_APPLICATION = 'wsgi.application'
# WSGI_APPLICATION = 'ws4redis.django_runserver.application'


# Context processors:
# https://docs.djangoproject.com/en/1.9/ref/templates/api/#built-in-template-context-processors
# django.template.backends.django.DjangoTemplates
# django.template.backends.jinja2.Jinja2
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [os.path.join(SITE_PATH, 'templates'), ],
        "APP_DIRS": True,
        "OPTIONS": {
            'environment': 'cms.core.jinja.environment',
            'trim_blocks': False,
            # "match_extension": ".jinja",
            # "context_processors": [
            #     "django.template.context_processors.request",
            #     # "django.contrib.auth.context_processors.auth",
            #     "django.template.context_processors.debug",
            #     "django.template.context_processors.i18n",
            #     # "django.template.context_processors.media",
            #     "django.template.context_processors.static",
            #     # "django.template.context_processors.tz",
            #     # "django.contrib.messages.context_processors.messages",
            # ],
        }
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            # "match_extension": ".html",
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                # "django.contrib.messages.context_processors.messages",
            ],
        }
    },
]

# from pashinin.celeryconfig import *
# try:
#     from pashinin.celeryconfig import *
# except:
#     print("celery (settings.py) import error!!!")

INSTALLED_APPS = (
    'redis_cache',                 # pip install django-redis-cache
    'channels',
    'bootstrap3',
    'cacheops',
    'django.contrib.auth',
    # 'polymorphic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # 'suit',                          # http://django-suit.readthedocs.org/en/latest/
    # 'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.postgres',
    'sortedm2m',
    # 'djcelery',
    'django_extensions',
    'django_nose',
    # 'django_jinja',
    'mptt',
    # 'django_pdb',
    # 'raven.contrib.django.celery',
    'raven.contrib.django.raven_compat',
    # 'social.apps.django_app.default',

    'pashinin',
)


WEBSOCKET_URL = '/_/ws/'

# channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
        'ROUTING': 'pashinin.routing.channel_routing',
    },
}

# admin panel bootstrap3 renderer
# DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'

# ./src/manage.py raven test
RAVEN_PUBLIC = ""
RAVEN_SECRET = ""

# http://raven.readthedocs.org/en/latest/transports/#sync
dsn_prefix = "sync+" if DEBUG else "threaded+"
# Transport selection via DSN is deprecated. You should explicitly pass
# the transport class to Client() instead.
# import raven
RAVEN_CONFIG = {
    'dsn': 'https://:@sentry.pashinin.com/2',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.dirname(__file__)),
}

import logging
from raven import Client
from raven.contrib.celery import register_signal, register_logger_signal
client = Client(RAVEN_CONFIG['dsn'])
register_logger_signal(client)
register_signal(client)
register_logger_signal(client, loglevel=logging.INFO)

# Tests
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TEST_RUNNER = 'django_pytest.test_runner.TestRunner'
if testing:
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

SOUTH_TESTS_MIGRATE = False  # To disable migrations and use syncdb instead
SKIP_SOUTH_TESTS = True      # To disable South's own unit tests

# http://vk.com/apps?act=manage


# Auth
AUTHENTICATION_BACKENDS = (
    'cms.core.backends.EmailBackend',
    # 'social.backends.google.GoogleOpenId',
    # 'social.backends.facebook.FacebookOAuth2',
    # 'social.backends.google.GoogleOAuth2',
    # 'social.backends.google.GoogleOAuth',
    'social.backends.vk.VKOAuth2',
    'social.backends.github.GithubOAuth2',
    # 'allauth.account.auth_backends.AuthenticationBackend',
)
SOCIAL_AUTH_USER_MODEL = 'user.CustomUser'

# Github
# https://github.com/settings/applications
# {% if sa_github_key is defined and sa_github_secret is defined %}
# SOCIAL_AUTH_GITHUB_KEY = ""
# SOCIAL_AUTH_GITHUB_SECRET = ""
# {% endif %}

# Facebook
# https://developers.facebook.com/apps
# {% if sa_facebook_key is defined and sa_facebook_secret is defined %}
# SOCIAL_AUTH_FACEBOOK_KEY = ''
# SOCIAL_AUTH_FACEBOOK_SECRET = ''
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']  # to get email
# {% endif %}

# Vkontakte
# http://vk.com/apps?act=manage
# http://vk.com/dev/permissions
# {% if sa_vk_key is defined and sa_vk_secret is defined %}
# SOCIAL_AUTH_VK_OAUTH2_KEY = ''
# SOCIAL_AUTH_VK_OAUTH2_SECRET = ''
# SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
# {% endif %}

# Google+
# https://console.developers.google.com/project
# Enable: Contacts API, Google+ API
# {% if sa_google_key is defined and sa_google_secret is defined %}
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
# {% endif %}

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

AUTH_USER_MODEL = 'user.CustomUser'
CUSTOM_USER_MODEL = 'user.CustomUser'

MIGRATION_MODULES = {
    'auth': None,
    # 'contenttypes': None,
    # 'default': None,
    # 'sessions': None,

    # 'core': None,
    # 'profiles': None,
    # 'snippets': None,
    # 'scaffold_templates': None,
}

SESSION_ENGINE = 'redis_sessions.session'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        # 'LOCATION': '/var/run/redis/redis-server.pid',
        'LOCATION': ['127.0.0.1:6379'],
        # 'KEY_PREFIX': 'd' if DEBUG else '',
    }
}
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING_CONFIG = 'logging.config.dictConfig'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # 'root': {
    #    'level': 'WARNING',
    #    'handlers': ['sentry'],
    # },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        # 'sentry': {
        #    'level': 'ERROR',
        #    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        #    #'class': 'raven.contrib.django.handlers.SentryHandler',
        # },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

import redis
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
# def show_toolbar(request):
#     return not request.is_ajax() and request.user and request.user.username == "yourusername"

if r.get('ddt')==b'True' and not DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = ('127.0.0.1', '10.254.239.2', '10.92.209.1')
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        # 'SHOW_TOOLBAR_CALLBACK': 'projectname.settings.show_toolbar',
    }

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        # 'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
            'debug_toolbar.panels.headers.HeadersPanel',
        # 'debug_toolbar.panels.profiling.ProfilingDebugPanel',
            'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        # 'debug_toolbar.panels.logger.LoggingPanel',
    )


# Directories for uploaded files
FILE_UPLOAD_TEMP_DIR = os.path.join(GIT_PATH, "files", "uploads")
max_download_size = 1024*1024*4

SENDFILE_ROOT = FILES_ROOT
SENDFILE_URL = '/_file'
SENDFILE_BACKEND = 'sendfile.backends.nginx'
APPEND_SLASH = True
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024*1024*3


CACHEOPS_REDIS = {
    'host': '127.0.0.1',  # redis-server is on same machine
    'port': 6379,            # default redis port
    'db': 0,                 # SELECT non-default redis database
                             # using separate redis db or redis instance
                             # is highly recommended
    'socket_timeout': 3,
}

CACHEOPS = {
    # Automatically cache any User.objects.get() calls for 15 minutes
    # This includes request.user or post.author access,
    # where Post.author is a foreign key to auth.User
    'auth.user': {'ops': 'get', 'timeout': 60*15},

    # Automatically cache all gets and queryset fetches
    # to other django.contrib.auth models for an hour
    'auth.*': {'ops': ('fetch', 'get'), 'timeout': 60*60},
    'cms.*': {'ops': ('fetch', 'get'), 'timeout': 60*60},
    'edu.*': {'ops': ('fetch', 'get'), 'timeout': 60*60},
    'user.*': {'ops': ('fetch', 'get'), 'timeout': 60*60},
    'db.*': {'ops': 'all', 'timeout': 60*60},
    'films.*': {'ops': 'all', 'timeout': 60*60},
    'torrents.*': {'ops': 'all', 'timeout': 60*60},

    # Cache gets, fetches, counts and exists to Permission
    # 'all' is just an alias for ('get', 'fetch', 'count', 'exists')
    'auth.permission': {'ops': 'all', 'timeout': 60*60},

    # Enable manual caching on all other models with default timeout of an hour
    # Use Post.objects.cache().get(...)
    #  or Tags.objects.filter(...).order_by(...).cache()
    # to cache particular ORM request.
    # Invalidation is still automatic
    '*.*': {'ops': (), 'timeout': 60*60},

    # And since ops is empty by default you can rewrite last line as:
    '*.*': {'timeout': 60*60},
}

if DEBUG:
    CACHEOPS_ENABLED = False