# -*- mode: python -*-
import os
import sys
import platform
import datetime
# import daphne.server
from raven import Client
from raven.contrib.celery import register_signal, register_logger_signal
from os.path import dirname, abspath, basename

SETTINGS_PATH = dirname(abspath(__file__))
APP = basename(SETTINGS_PATH)
REPO_PATH = dirname(dirname(SETTINGS_PATH))  # GIT_PATH
REPOS_PATH = dirname(REPO_PATH)
VEBIN = os.path.join(REPO_PATH, "tmp", "ve", "bin")
VEPYTHON = os.path.join(REPO_PATH, "tmp", "ve", "bin", "python")
PYPY = platform.python_implementation() == 'PyPy'
TRAVIS = os.getenv('TRAVIS') == 'true'
TESTING = os.getenv('TRAVIS') or (
    'test' in sys.argv or
    '--reuse-db' in sys.argv or
    '--durations=3' in sys.argv
)
DOCKER = os.getenv('DOCKER') == 'true'

if TRAVIS:
    DEBUG = os.getenv('DEBUG') == 'true'
else:
    DEBUG = DOCKER
    if TESTING:
        DEBUG = False
# DEBUG = False

# Vault's data
secret = {}  # all secrets, loaded from Vault
if not (DEBUG or TRAVIS or DOCKER):
    try:
        role_id = os.getenv('ROLE_ID')
        if not role_id:
            role_id = open(os.path.join(
                REPO_PATH,
                'tmp',
                'role'
            )).read()
        secret_id = os.getenv('SECRET_ID')
        import hvac
        vault = hvac.Client(url='http://vault.service.consul:8200')
        # App Role
        vault.auth_approle(role_id, secret_id)
        secret = vault.read('secret/pashinin.com')['data']
    except Exception as e:
        print(e)
        # raise


EMAIL_HOST = '10.254.239.4'
# EMAIL_TIMEOUT = 5  # in seconds
EMAIL_PORT = 25
# EMAIL_USE_SSL = True


# If you have a mail server - error messages are posted to admins
ADMINS = (
    ('Admin', 'sergey@pashinin.com'),
)
MANAGERS = ADMINS
DOMAIN = "pashinin.com"
SERVER_EMAIL = f'Error <robot@{DOMAIN}>'      # "From" field
DEFAULT_HOST = APP
HOST_PORT = ''
if DOCKER:
    DOMAIN = 'localhost'

    # django_hosts
    #
    # The port to append to host names during reversing,
    # https://django-hosts.readthedocs.io/en/latest/#django.conf.settings.HOST_PORT
    HOST_PORT = '8000'

# PARENT_HOST = DOMAIN  # django_hosts

# Databases
#
# django.db.backends.postgresql_psycopg2
# django.contrib.gis.db.backends.postgis
#
try:
    import psycopg2
except ImportError:
    # Fall back to psycopg2cffi (for PyPy)
    from psycopg2cffi import compat
    compat.register()
DB_ENGINE = 'django.db.backends.postgresql_psycopg2'
DB_HOST = 'db' if DOCKER else '127.0.0.1'
DB_PORT = '5432' if DOCKER or TRAVIS else '25432'  # Stolon
DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': "pashinin" if DOCKER else secret.get('dbname'),
        'USER': "pashinin" if DOCKER else secret.get('dbuser'),
        'PASSWORD': "superpass" if DOCKER else secret.get('dbpass'),
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        # PORT
        # 5432 - postgres
        # 6432 - pgbouncer
        'CONN_MAX_AGE': 0 if DEBUG else None,  # persistent DB connections
    },
    'sentry': {
        'ENGINE': DB_ENGINE,
        'NAME': "sentry",
        'USER': "pashinin" if DOCKER else secret.get('dbuser'),
        'PASSWORD': "superpass" if DOCKER else secret.get('dbpass'),
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'CONN_MAX_AGE': 0 if DEBUG else None,  # persistent DB connections
    },
}


TELEGRAM_TOKEN = '' if DOCKER or TRAVIS else secret.get('telegrambot_token')

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    f'.{DOMAIN}',
    'localhost',
    'example.org',
    # "*",
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
if DEBUG:
    SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
# USE_I18N = True
USE_I18N = False

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# ugettext = lambda s: s
LANGUAGES = (
    ('en-us', 'English'),
    ('en', 'English'),
    ('ru', 'Russian'),
)

LOCALE_PATHS = (
    # 'locale',
    os.path.join(SETTINGS_PATH, 'locale'),
)

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False       # needs to be False for DATETIME_FORMAT to work

# If you set this to False, Django will not use timezone-aware datetimes.
#
# Celery has some problems with "USE_TZ = True"
# https://github.com/celery/django-celery-beat/pull/68
#
# Django docs recommends setting it to True
USE_TZ = True
# https://github.com/celery/celery/issues/4169


DATETIME_FORMAT = "Y-m-d H:i:sO"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/_sp/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(REPO_PATH, "static")


# if not os.path.isdir(FILES_ROOT) and TESTING:
#     FILES_ROOT = os.path.join(REPO_PATH, 'tmp', 'files')
#     if not os.path.isdir(FILES_ROOT):
#         os.makedirs(FILES_ROOT, exist_ok=True)
FILES_ROOT = [
    "/mnt/ceph/files",
    # "{{FILES_ROOT}}",
]
if TESTING or DEBUG:
    FILES_ROOT = [os.path.join(REPO_PATH, 'tmp', 'files')]


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
# if isinstance(FILES_ROOT, str):
#     MEDIA_ROOT = os.path.join(FILES_ROOT, 'uploads/')
# else:
MEDIA_ROOT = os.path.join(FILES_ROOT[0], 'uploads/')

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

# Use ManifestStaticFilesStorage for static files versioning
# (instead of manually writing file.min.js?v=1.2.3)
#
# 1. Works only if DEBUG=false
# 2. Do not forget to run "collectstatic"
#
# Default: 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_STORAGE = 'core.static_storage.StaticStorage'
if DEBUG or TESTING:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a' if DOCKER else secret.get('SECRET_KEY')

# Auth once on all subdomains
SESSION_COOKIE_DOMAIN = '.'+DOMAIN
if DEBUG or DOCKER:
    SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_NAME = 'session'
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False

# To auth once at many domains (not subdomains) - look for SSO
# (single sing on).


LOGIN_URL = '/login'

# MIDDLEWARE_CLASSES = (
MIDDLEWARE = [
    # 'django_hosts.middleware.HostsRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    # Before any middleware that may change the response (it sets the
    # Content-Length header). A middleware that appears before
    # CommonMiddleware and changes the response must reset
    # Content-Length.
    'django.middleware.common.CommonMiddleware',

    # 'django.middleware.csrf.CsrfViewMiddleware',

    # Auth
    #
    # After SessionMiddleware: uses session storage.
    #
    # AuthenticationMiddleware on Github:
    # https://github.com/django/django/blob/master/django/contrib/auth/middleware.py
    #
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'graphql_jwt.middleware.JSONWebTokenMiddleware',
    # 'core.auth.AuthenticationMiddleware',

    # Wrap the every request that isn’t GET, HEAD or OPTIONS in a
    # revision block:
    'reversion.middleware.RevisionMiddleware',

    # Admin panel does not work without messages:
    'django.contrib.messages.middleware.MessageMiddleware',

    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django_pdb.middleware.PdbMiddleware',

    # 'django_hosts.middleware.HostsResponseMiddleware',
]


CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'github.com',
    'localhost',
    '127.0.0.1'
)

ROOT_URLCONF = f'{APP}.urls'

# Context processors:
# https://docs.djangoproject.com/en/1.9/ref/templates/api/#built-in-template-context-processors
# django.template.backends.django.DjangoTemplates
# django.template.backends.jinja2.Jinja2
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [
            os.path.join(REPO_PATH, 'templates'),
            os.path.join(SETTINGS_PATH, 'templates'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            'environment': 'core.jinja.environment',
            'trim_blocks': False,
        }
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(REPO_PATH, 'templates'),
        ],
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


REDIS_PORT = 6379
REDIS_SERVER = 'redis' if DOCKER else '127.0.0.1'

DYNOMITE_PORT = 6379 if DOCKER or TRAVIS else 8102
DYNOMITE_SERVER = 'redis' if DOCKER else '127.0.0.1'

# Celery settings
BROKER_URL = f'redis://{REDIS_SERVER}:{REDIS_PORT}/0'
# BROKER_URL = "amqp://admin:mypass@rabbit:5672/%2F"

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)


# ------------ Celery --------------
# This file is a part of Django's settings.py. It is included withing
# it.
#
# from celery.schedules import crontab
# from datetime import timedelta
# from django.conf import settings

# Register our serializer methods into kombu
# from kombu.serialization import register
# from core.json import my_dumps, my_loads
# register('myjson', my_dumps, my_loads,
#          content_type='application/json',
#          content_encoding='utf-8')

# If this is True, all tasks will be executed locally by blocking
# until the task returns.
#
# ! USE IN DEBUG ONLY !
#
# Use it only if you don't have a worker running, docker-compose starts
# 1 worker (see docker-compose.yml):
#
# CELERY_ALWAYS_EAGER = DEBUG

# CELERY_RESULT_BACKEND = 'redis://'
# CELERY_RESULT_BACKEND = 'redis://{{redis_server}}:6379/0'
# CELERY_RESULT_BACKEND = BROKER_URL
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'django-cache'


# Add a one-minute timeout to all Celery tasks.
# TODO: Can I detect soft timeout in a task?
CELERYD_TASK_SOFT_TIME_LIMIT = 60

# Tell celery to use your new serializer:
# CELERY_ACCEPT_CONTENT = ['myjson']
# CELERY_TASK_SERIALIZER = 'myjson'
# CELERY_RESULT_SERIALIZER = 'myjson'

# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

CELERYD_POOL_RESTARTS = True
CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_SENT_EVENT = True


# Fixed in Celery 4.2.0 (not published yet)
# Problems if have TZ = TZ from Django project settings file
# 1. https://github.com/celery/celery/issues/4184
# 2. https://github.com/celery/celery/issues/4177
# 3. https://github.com/celery/celery/issues/4169
# CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True


# Please do not touch (and change) my logger, Celery!
# If Sentry logging in Django/Celery stopped working use:
CELERYD_HIJACK_ROOT_LOGGER = False
# ------------ end Celery --------------


TASTYPIE_DEFAULT_FORMATS = ['json']

GRAPHENE = {
    'SCHEMA': 'index.schema.SCHEMA'  # Where your Graphene schema lives
}


INSTALLED_APPS = (
    # 'tastypie',
    # 'django_filters',
    'graphene_django',

    # 'django_hosts',  # for subdomains
    # 'redis_cache',                 # pip install django-redis-cache
    'django_redis',

    'channels',
    'channels_api',

    'ordered_model',

    'cacheops',
    # 'django_pickling',  # for cacheops - make pickeling faster

    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    # Admin panel does not work without messages:
    'django.contrib.messages',

    # 'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # required by django-allauth
    'django.contrib.sitemaps',

    'django.contrib.admin',  # with apps autodiscover
    # 'django.contrib.admin.apps.SimpleAdminConfig'  # no autodiscover

    'django.contrib.postgres',
    'sortedm2m',

    # 'django_celery_beat',
    'django_celery_beat.apps.BeatConfig',
    'django_celery_results',

    'django_extensions',  # shell_plus, runserver_plus, ...
    'rest_framework',
    'django_nose',
    'mptt',
    'raven.contrib.django.raven_compat',
    # 'lazysignup',
    'reversion',
    # 'social.apps.django_app.default',

    # 'mama_cas',
    # 'django_cas_ng',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # # VK - manage apps here: https://vk.com/apps?act=manage
    'allauth.socialaccount.providers.vk',
)
MY_APPS = (
    'core',
    # 'core.asgi_kafka',
    'core.files',
    'baumanka',
    'articles',
    'edu',
    'ege',
    'pashinin',
)
INSTALLED_APPS += MY_APPS
if APP not in INSTALLED_APPS:
    INSTALLED_APPS += (APP, )

REST_FRAMEWORK = {
    # TokenAuthentication needed to remove CSRF errors
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'DEFAULT_PAGINATION_CLASS': 'core.CursorPagination',
    'PAGE_SIZE': 10,

    # REST: Disable GET API web view (GET request) globally
    #
    # 1. For 1 APIView add "renderer_classes = [renderers.JSONRenderer]"
    # to this view
    #
    # 2. For all views:
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # )

    # Default:
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    #     'rest_framework.renderers.BrowsableAPIRenderer',
    # )

    # TODO:
    # pip install ujson
    # pip install drf_ujson
    # 'DEFAULT_RENDERER_CLASSES': (
    #    'drf_ujson.renderers.UJSONRenderer',
    # )
    # 'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S%z",
}
# REST_USE_JWT = True

JWT_AUTH = {
    # 'JWT_ENCODE_HANDLER':
    # 'rest_framework_jwt.utils.jwt_encode_handler',

    # 'JWT_DECODE_HANDLER':
    # 'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    # 'rest_framework_jwt.utils.jwt_payload_handler',
    'auth.jwt_payload_handler',

    # 'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    # 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    # 'JWT_RESPONSE_PAYLOAD_HANDLER':
    # 'rest_framework_jwt.utils.jwt_response_payload_handler',

    # 'JWT_SECRET_KEY': settings.SECRET_KEY,
    # 'JWT_GET_USER_SECRET_KEY': None,
    # 'JWT_PUBLIC_KEY': None,
    # 'JWT_PRIVATE_KEY': None,
    # 'JWT_ALGORITHM': 'HS256',
    # 'JWT_VERIFY': True,
    # 'JWT_VERIFY_EXPIRATION': True,
    # 'JWT_LEEWAY': 0,
    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 'JWT_AUDIENCE': None,
    # 'JWT_ISSUER': None,

    # 'JWT_ALLOW_REFRESH': False,
    'JWT_ALLOW_REFRESH': True,
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    # 'JWT_AUTH_HEADER_PREFIX': 'JWT',
    # 'JWT_AUTH_COOKIE': None,
}


if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
    )

WEBSOCKET_URL = '/_/ws/'

# channels
CHANNEL_LAYERS = {
    'default': {
        'ROUTING': f'{APP}.routing.channel_routing',
        # 'ROUTING': app+'.routing.application',
        # "BACKEND": "core.asgi_kafka.KafkaChannelLayer",
        # "CONFIG": {
        #     "url": "amqp://kafka:9092/pashinincom",
        # },

        # RabbitMQ
        # "BACKEND": "asgi_rabbitmq.RabbitmqChannelLayer",
        # "CONFIG": {
        #     "url": "amqp://guest:guest@rabbit:5672/pashinincom?heartbeat_interval=15",
        # },


        # "BACKEND": "asgi_redis.RedisSentinelChannelLayer",  # HA: Redis + Slave + Slave + Sentinel
        'BACKEND': 'asgi_redis.RedisChannelLayer',  # Single Redis server
        'CONFIG': {
            'hosts': [(REDIS_SERVER, REDIS_PORT)],

            # "prefix" is needed when you have several "Django
            # channels"-powered projects on the same host (same redis
            # db)
            "prefix": '{APP}.{DOMAIN}{SITE_ID}',
        },
    },
}
# CHANNEL_LAYERS = {}
ASGI_APPLICATION = f"{APP}.routing.application"


# admin panel bootstrap3 renderer
DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'


# ./src/manage.py raven test
RAVEN_PUBLIC = '' if DOCKER else '52241091d32f4260af10014634c527fb'
RAVEN_SECRET = secret.get('raven_secret')

# http://raven.readthedocs.org/en/latest/transports/#sync
# dsn_prefix = "sync+" if DEBUG else "threaded+"
# Transport selection via DSN is deprecated. You should explicitly pass
# the transport class to Client() instead.
# import raven
if not TESTING and not DEBUG:
    RAVEN_CONFIG = {
        'dsn': f'https://{RAVEN_PUBLIC}:{RAVEN_SECRET}@sentry.{DOMAIN}/2',
        # If you are using git, you can also automatically configure the
        # release based on the git info.
        # 'release': raven.fetch_git_sha(os.path.dirname(__file__)),
    }

# Uncomment 4 lines below
# client = Client(RAVEN_CONFIG['dsn'])
# register_logger_signal(client)
# register_signal(client)
# register_logger_signal(client, loglevel=logging.INFO)

if TESTING:
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )


# If a backend raises a PermissionDenied exception, authentication will
# immediately fail. Django won’t check the backends that follow.
AUTHENTICATION_BACKENDS = [
    # 'graphql_jwt.backends.JSONWebTokenBackend',
    # 'rules.permissions.ObjectPermissionBackend',

    # ModelBackend on Github:
    # https://github.com/django/django/blob/master/django/contrib/auth/backends.py
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# http://django-allauth.readthedocs.io/en/latest/advanced.html#custom-user-models
# allauth stuff:
if DEBUG:
    ACCOUNT_LOGIN_ATTEMPTS_LIMIT = None
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_AUTO_SIGNUP = True


SOCIAL_AUTH_USER_MODEL = 'core.User'

CAS_SERVER_URL = '//'+DOMAIN+'/cas/'

# Github
# https://github.com/settings/applications
# {% if sa_github_key is defined and sa_github_secret is defined %}
# SOCIAL_AUTH_GITHUB_KEY = "{{sa_github_key}}"
# SOCIAL_AUTH_GITHUB_SECRET = "{{sa_github_secret}}"
# {% endif %}

# Facebook
# https://developers.facebook.com/apps
# {% if sa_facebook_key is defined and sa_facebook_secret is defined %}
# SOCIAL_AUTH_FACEBOOK_KEY = '{{sa_facebook_key}}'
# SOCIAL_AUTH_FACEBOOK_SECRET = '{{sa_facebook_secret}}'
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']  # to get email
# {% endif %}

# Vkontakte
# http://vk.com/apps?act=manage
# http://vk.com/dev/permissions
# {% if sa_vk_key is defined and sa_vk_secret is defined %}
# SOCIAL_AUTH_VK_OAUTH2_KEY = '{{sa_vk_key}}'
# SOCIAL_AUTH_VK_OAUTH2_SECRET = '{{sa_vk_secret}}'
# SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
# {% endif %}

# Google+
# https://console.developers.google.com/project
# Enable: Contacts API, Google+ API
# {% if sa_google_key is defined and sa_google_secret is defined %}
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '{{sa_google_key}}'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '{{sa_google_secret}}'
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

AUTH_USER_MODEL = 'core.User'

# https://docs.djangoproject.com/en/1.10/ref/settings/#migration-modules
MIGRATION_MODULES = {
    # 'auth': None,
    # 'contenttypes': None,
    # 'default': None,
    # 'sessions': None,

    # 'core': None,
    # 'profiles': None,
    # 'snippets': None,
    # 'scaffold_templates': None,
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
# SESSION_COOKIE_AGE =

SESSION_REDIS_HOST = DYNOMITE_SERVER
SESSION_REDIS_PORT = DYNOMITE_PORT

CACHES = {
    'default': {
        # 'BACKEND': 'redis_cache.RedisCache',  # django-redis-cache
        'BACKEND': 'django_redis.cache.RedisCache',  # django-redis  (active development)
        "LOCATION": f'redis://{DYNOMITE_SERVER}:{DYNOMITE_PORT}/0',
        'KEY_PREFIX': 't' if TESTING else '',
        # TIMEOUT:300,  # Default: 300
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            "SOCKET_TIMEOUT": 5,  # in seconds
        }
    }
}

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#
# version - ?
# disable_existing_loggers -
#
# levels:
# DEBUG: Low level system information for debugging purposes
# INFO: General system information
# WARNING: Information describing a minor problem that has occurred.
# ERROR: Information describing a major problem that has occurred.
# CRITICAL: Information describing a critical problem that has occurred.
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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
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
    # propagate
    #
    # Propagate or not messages. This means that log messages written to
    # "core.views" will not be handled by the "core" logger.
    'loggers': {
        # 'django.request': {
        'django': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },


        # If you uncomment it then log messages from "core" will be displayed
        # twice. For 'core' and '' loggers.
        # 'core': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },

        # About "catch-all" logger:
        # 1. This is ultra-slow and buggy with RabbitMQ as channels broker
        #    (for example)
        # 2. It will output any debug messages (log.debug() calls) from any
        #    3rd party library like: rabbitmq, daphne, ... anything else
        # => Disabled it
        # when enabled I used: logging.getLogger("pika").setLevel(logging.INFO)
        # to disable "pika" rabbitmq logger
        # '': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
    }
}
for APP in MY_APPS:
    LOGGING['loggers'][APP] = {
        'handlers': ['console'] if DEBUG else ['mail_admins'],
        'level': 'DEBUG' if DEBUG else 'WARNING',
        'propagate': True,

        # 'propagate': True, causes printing messages several times. For
        # example if a message fired in 'core.files' app it will be printed
        # 2nd time for 'core' app logger.
        # But I enabled it because missed:
        #
        # ValueError: Missing staticfiles
        # manifest entry for '/core_files.min.js'
    }

# Whether to store the CSRF token in the user’s session instead of in a cookie.
# It requires the use of django.contrib.sessions.
#
# Storing the CSRF token in a cookie (Django’s default) is safe,
# but storing it in the session is common practice in other web frameworks
# and therefore sometimes demanded by security auditors.
# CSRF_USE_SESSIONS = True


# Directories for uploaded files
# FILE_UPLOAD_TEMP_DIR = os.path.join(REPO_PATH, "tmp", "uploads")
# max_download_size = 1024*1024*4

SENDFILE_ROOT = FILES_ROOT[0]
SENDFILE_URL = '/_file'
SENDFILE_BACKEND = 'sendfile.backends.nginx'
APPEND_SLASH = True


FILE_UPLOAD_MAX_MEMORY_SIZE = 1024*1024*3
# FILE_UPLOAD_HANDLERS¶
# Default:

# [
#     'django.core.files.uploadhandler.MemoryFileUploadHandler',
#     'django.core.files.uploadhandler.TemporaryFileUploadHandler',
# ]


# if DEBUG:
CACHEOPS_ENABLED = False

CACHEOPS_REDIS = {
    'host': DYNOMITE_SERVER,  # redis-server is on same machine
    'port': DYNOMITE_PORT,    # default redis port
    'db': 0,                  # SELECT non-default redis database
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
    'core.*': {'ops': ('fetch', 'get'), 'timeout': 60*60},
    'edu.*': {'ops': ('fetch', 'get'), 'timeout': 60*60},
    'user.*': {'ops': ('fetch', 'get'), 'timeout': 60*60},
    'db.*': {'ops': 'all', 'timeout': 60*60},

    # Cache gets, fetches, counts and exists to Permission
    # 'all' is just an alias for ('get', 'fetch', 'count', 'exists')
    'auth.permission': {'ops': 'all', 'timeout': 60*60},

    # Enable manual caching on all other models with default timeout of an hour
    # Use Post.objects.cache().get(...)
    #  or Tags.objects.filter(...).order_by(...).cache()
    # to cache particular ORM request.
    # Invalidation is still automatic
    # '*.*': {'ops': (), 'timeout': 60*60},

    # And since ops is empty by default you can rewrite last line as:
    '*.*': {'timeout': 60*60},
}

SHELL_PLUS_PRE_IMPORTS = [
    # ('module.submodule1', ('class1', 'function2')),
    # ('module.submodule2', 'function3'),
    # ('module.submodule3', '*'),
    # 'module.submodule4'
    ('django.core.management', ('call_command', ))
]

CHANNELS_API = {
    'DEFAULT_PAGE_SIZE': 5,
    'CHECK_ALL_PERMISSIONS': False,
    # 'DEFAULT_PERMISSION_CLASSES': ('channels_api.permissions.AllowAny', ),
    'DEFAULT_PERMISSION_CLASSES': ('channels_api.permissions.IsSuperuser', ),
    # 'DEFAULT_PERMISSION_CLASSES': tuple(),
}

try:
    del secret
except NameError:
    pass
