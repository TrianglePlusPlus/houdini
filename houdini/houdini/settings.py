"""
Django settings for houdini project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from datetime import timedelta

from django.contrib.messages import constants as messages_constants

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ROOT = os.path.dirname(BASE_DIR)
# STATIC_ROOT = os.path.join(ROOT, 'static')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# TODO: do not enable this setting unless you your houdini app is behind a proxy server,
# and your proxy strips the X-Forwarded-Proto header from all incoming requests
# and sets the X-Forwarded-Proto header only for requests that originally come in via HTTPS!
# see: https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-SECURE_PROXY_SSL_HEADER
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# TODO: hopefully this one will eventually be handled by the web server
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# TODO: looks like these next two are now handled by the web server
SECURE_HSTS_SECONDS = 600 # TODO: should eventually be set to something like 31536000 (1 year)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SSL_DEV_CERT_KEY = (os.getenv('SSL_DEV_CERT'), os.getenv('SSL_DEV_KEY'))

HOUDINI_KEY = os.getenv('app_key')
HOUDINI_SECRET = os.getenv('app_secret')
HOUDINI_SERVER = os.getenv('houdini_server')
ISO_8601 = "%Y-%m-%dT%H:%M:%S"
TIME_TO_LIVE = timedelta(weeks=1)
ACCOUNT_ACTIVATION_TIME = timedelta(days=1)
PASSWORD_RESET_TIME = timedelta(days=1)

# Email
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL') == 'True'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMINS = (
    ('Justice Suh', 'justice.suh@gmail.com'),
)


AUTH_USER_MODEL = 'houdini_admin.User'
AUTHENTICATION_BACKENDS = ['houdini_client.auth_backend.RemoteServerAuthBackend']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'houdini_admin',
    # We import the AppConfig so that it can set up its signals
    'houdini_server.apps.HoudiniServerConfig',
    'houdini_client',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'houdini_client.middleware.AuthenticationMiddleware'
]

ROOT_URLCONF = 'houdini.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'houdini.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.getenv('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'


MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_TAGS = {
    messages_constants.ERROR: 'danger'
}

