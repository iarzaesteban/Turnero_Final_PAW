from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '92e9-2800-af0-150a-bba2-e9d1-16e3-def6-5259.ngrok-free.app']
CSRF_TRUSTED_ORIGINS = ['https://92e9-2800-af0-150a-bba2-e9d1-16e3-def6-5259.ngrok-free.app']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASSWORD'),
        'HOST': 'db_postgres',
        'PORT': '5432',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')