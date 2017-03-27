"""
Django settings for RTTWebInterface project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import configparser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(BASE_DIR, "credentials/secret_key")) as f:
    SECRET_KEY = f.read().rstrip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'ViewResults.apps.ViewresultsConfig',
    'SubmitExperiment.apps.SubmitexperimentConfig',
    'Administration.apps.AdministrationConfig',
    'bootstrap3',
    'bootstrapform',
    'datetimewidget',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'RTTWebInterface.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'RTTWebInterface.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
default_db_cred_file = os.path.join(BASE_DIR, "credentials/default_db_credentials.ini")
default_db_cred = configparser.ConfigParser()
default_db_cred.read(default_db_cred_file)
if len(default_db_cred.sections()) == 0:
    raise FileNotFoundError("can't read credentials: {}".format(default_db_cred_file))

rtt_db_cred_file = os.path.join(BASE_DIR, "credentials/rtt_db_credentials.ini")
rtt_db_cred = configparser.ConfigParser()
rtt_db_cred.read(rtt_db_cred_file)
if len(rtt_db_cred.sections()) == 0:
    raise FileNotFoundError("can't read credentials: {}".format(rtt_db_cred_file))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': default_db_cred.get('Credentials', 'Name'),
        'USER': default_db_cred.get('Credentials', 'User'),
        'PASSWORD': default_db_cred.get('Credentials', 'Password'),
        'HOST': default_db_cred.get('Credentials', 'Host'),
        'PORT': default_db_cred.get('Credentials', 'Port'),
    },
    'rtt-database': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': rtt_db_cred.get('Credentials', 'Name'),
        'USER': rtt_db_cred.get('Credentials', 'User'),
        'PASSWORD': rtt_db_cred.get('Credentials', 'Password'),
        'HOST': rtt_db_cred.get('Credentials', 'Host'),
        'PORT': rtt_db_cred.get('Credentials', 'Port'),
        'OPTIONS': {
            'autocommit': False,
        },
    }
}

del rtt_db_cred
del default_db_cred

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

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# For file uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
