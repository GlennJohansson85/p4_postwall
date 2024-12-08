# settings.py
import os
from pathlib import Path
import dj_database_url

# Load environment variables from env.py
if os.path.isfile('env.py'):
    import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Django
SECRET_KEY = os.environ.get('SECRET_KEY', '')

DEBUG = True

ALLOWED_HOSTS = [
    'p4postwall-4a255b5600ea.herokuapp.com',
    'localhost',
    '127.0.0.1'
]

CSRF_TRUSTED_ORIGINS = [
    'https://p4postwall-4a255b5600ea.herokuapp.com'
]

AUTH_USER_MODEL = 'accounts.Profile'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'accounts',
    'storages',
    'gunicorn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'p4_postwall.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'django.template.context_processors.static',
            ],
        },
    },
]


WSGI_APPLICATION = 'p4_postwall.wsgi.application'


from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Intern.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Email Conf.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Local Static & Media Configuraiton
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Deployed Static & Media Configuration
if 'USE_AWS' in os.environ:
    AWS_STORAGE_BUCKET_NAME = 'p4postwall'
    AWS_S3_REGION_NAME      = 'eu-north-1'
    AWS_ACCESS_KEY_ID       = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY   = os.environ.get('AWS_SECRET_ACCESS_KEY')

    # Dynamic custom domain
    AWS_S3_CUSTOM_DOMAIN    = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

    # Explicit location configuration for static and media
    STATICFILES_LOCATION    = 'static'
    MEDIAFILES_LOCATION     = 'media'

    # Storage classes
    STATICFILES_STORAGE     = 'custom_storages.StaticStorage'
    DEFAULT_FILE_STORAGE    = 'custom_storages.MediaStorage'

    # URLs for static and media files
    STATIC_URL              = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    MEDIA_URL               = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
