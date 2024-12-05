import os
from pathlib import Path
import dj_database_url

# Load environment variables from env.py
if os.path.isfile('env.py'):
    import env


BASE_DIR = Path(__file__).resolve().parent.parent

# Django
SECRET_KEY = os.environ.get('SECRET_KEY', '')

DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'p4postwall-4a255b5600ea.herokuapp.com',
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
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'accounts.context_processors.profile_context',
            ],
        },
    },
]


WSGI_APPLICATION = 'p4_postwall.wsgi.application'


from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# DATABASE (SQLite by default, switches to Postgres in production)
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = True
#EMAIL_PORT = 587
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Static and media file handling for local development
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# AWS S3 Configuration
if os.environ.get('USE_AWS') == 'True':
    AWS_S3_OBJECT_PARAMETERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
    }

    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"  # Dynamic custom domain

    # Static and media files storage classes
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'  # Ensure correct storage class for media
    MEDIAFILES_LOCATION = 'media'

    # Override static and media URLs in production
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

else:
    # Local file storage for static and media in development
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
