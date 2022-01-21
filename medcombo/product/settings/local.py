from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'localdb'),
    }
}

THIRD_PARTY_APPS = (
    'debug_toolbar',
)

INSTALLED_APPS += THIRD_PARTY_APPS

# django debug toolbar

INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CUSTOM = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

MIDDLEWARE+=MIDDLEWARE_CUSTOM
# ------------------------------------

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

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

""" AWS_ACCESS_KEY_ID = 'AKIAQE37QMQ7M6QDVJ57'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'static-test-mc-s3'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
} """

# AWS_LOCATION = 'media'

# AWS_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# DEFAULT_FILE_STORAGE = 'medcombo.settings.storage_backends.MediaStorage'

# MEDIA_URL = AWS_URL + 'media/'