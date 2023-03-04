"""
Django settings for pigscanfly project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os

from typing import *

from pathlib import Path

from configurations import Configuration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Base(Configuration):
    COOKIE_CONSENT_ENABLED = True
    COOKIE_CONSENT_LOG_ENABLED = True
    LOGIN_URL = 'login'
    LOGIN_REDIRECT_URL = '/'
    THUMBNAIL_DEBUG = True

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-4b6t3cnic_(g*0cexqe8w)=1&vyb#(erhad#7@y4sv)jzb2kaf'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    MEDIA_ROOT = "media"
    MEDIA_URL = '/media/'

    NEWSLETTER_THUMBNAIL = 'sorl-thumbnail'

    ALLOWED_HOSTS: List[str] = ['*']

    GOOGLE_CLIENT_SECRETS_FILE = os.getenv(
        "GOOGLE_CLIENT_SECRETS_FILE",
        "client_secret.json")

    if not os.path.exists(GOOGLE_CLIENT_SECRETS_FILE):
        GOOGLE_CLIENT_SECRETS_FILE = "../cal-sync-magic/client_secret.json"

    if not os.path.exists(GOOGLE_CLIENT_SECRETS_FILE):
        GOOGLE_CLIENT_SECRETS_FILE = "client_secret/client_secret.json"

    # If we don't have a secret file but we have the text make it.
    if not os.path.exists(GOOGLE_CLIENT_SECRETS_FILE):
        secret = os.getenv("GOOGLE_CLIENT_SECRETS_TEXT")
        if secret is not None:
            with open(GOOGLE_CLIENT_SECRETS_FILE, 'w') as f:
                f.write(secret)
                print(f"Success! Wrote {GOOGLE_CLIENT_SECRETS_FILE}")
        else:
            raise Exception(f"Error writing out secret, no client secret env var")

    # Application definition

    SITE_ID=1

    TEMPLATE_CONTEXT_PROCESSORS = [
        'django.template.context_processors.request']

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'main',
        'sorl.thumbnail',
        'easy_thumbnails',
        'newsletter',
        'cookie_consent',
        "compressor",
        'django_extensions',
        "cal_sync_magic",
        "static_thumbnails",
    ]

    COMPRESS_JS_FILTERS = [
        'compressor.filters.jsmin.JSMinFilter',
        'compressor.filters.yuglify.YUglifyJSFilter',
    ]

    STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "compressor.finders.CompressorFinder",
    )
    COMPRESS_ENABLED = True
    COMPRESS_OFFLINE = True
    COMPRESS_YUGLIFY_BINARY = "yuglify"
    COMPRESS_YUGLIFY_JS_ARGUMENTS = "--mangle"

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        "cookie_consent.middleware.CleanCookiesMiddleware",
        'django_user_agents.middleware.UserAgentMiddleware',
    ]

    GOOGLE_ANALYTICS = {
        'google_analytics_id': 'G-2EDT623L0V',
    }

    ROOT_URLCONF = 'pigscanfly.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / "templates"],
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

    WSGI_APPLICATION = 'pigscanfly.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/4.0/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    # MEDIA FILE SETTINGS

    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # STRIPE SETTINGS
    STRIPE_API_KEY = "sk_test_51MGgqqH3tqhFx4rg3scW0nEbQgv4aXCCvjdWkSYcCA5F15akyusRbkU6lzlIqW6XQmCSDvW9CKgKWmWFqyav5zs100rcmjUUDL"


class Dev(Base):
    Debug = True

    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


class Prod(Base):

    @property
    def SECRET_KEY(self):
        return os.getenv("SECRET_KEY")

    @property
    def STRIPE_API_KEY(self):
        return os.getenv("STRIPE_LIVE_SECRET_KEY")

    @property
    def DATABASES(self):
        engine = "django.db.backends.mysql"
        return {
            "default": {
                "ENGINE": engine,
                "NAME": os.getenv("DBNAME"),
                "USER": os.getenv("DBUSER"),
                "PASSWORD": os.getenv("DBPASSWORD"),
                "HOST": os.getenv("DBHOST"),
                "ATOMIC_REQUESTS": os.getenv("ATOMIC_REQUEST", False),
            }
        }

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv("EMAIL_HOST", "pigscanfly.ca")
    EMAIL_USE_TLS = True
    EMAIL_PORT = 25
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "support")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
    DEFAULT_FROM_EMAIL = "support@pigscanfly.ca"
