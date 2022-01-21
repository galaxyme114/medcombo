from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'postgres',
          'USER': 'postgres',
          'PASSWORD': 'postgres',
          'HOST': 'db',
          'PORT': '5432',
      }
    }


THIRD_PARTY_APPS = (
    'debug_toolbar',
)

INSTALLED_APPS += THIRD_PARTY_APPS

# django debug toolbar

INTERNAL_IPS = ('0.0.0.0',)

MIDDLEWARE_CUSTOM = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

MIDDLEWARE+=MIDDLEWARE_CUSTOM
# ------------------------------------
STATIC_ROOT = os.path.join(BASE_DIR, 'static2')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

CHAT_WS_SERVER_HOST = '0.0.0.0'
CHAT_WS_SERVER_PORT = 5002
CHAT_WS_SERVER_PROTOCOL = 'ws'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
STATIC_URL = '/static/'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': '',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            }
        },
    }
}

