from .base import *


DEBUG = False
ALLOWED_HOSTS = ['www.medcombo.com', 'medcombo.com']

DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'postgres',
          'USER': 'postgres',
          'PASSWORD': 'medpost10',
          'HOST': 'db',
          'PORT': '5432',
      }
    }

INTERNAL_IPS = ('0.0.0.0',)

THIRD_PARTY_APPS = (
    'storages',
)

INSTALLED_APPS += THIRD_PARTY_APPS

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
#STATIC_URL = 'http://ec2-3-133-109-99.us-east-2.compute.amazonaws.com/static/'
STATIC_URL = '/static/'

#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

AWS_ACCESS_KEY_ID = 'AKIAQE37QMQ7L4ZMGPAY'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'static-production-mc-s3'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'media'

AWS_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

DEFAULT_FILE_STORAGE = 'medcombo.settings.storage_backends.MediaStorage'

MEDIA_URL = AWS_URL + 'media/'
