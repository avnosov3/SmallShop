from pathlib import Path

import environ

from shop.apps import ShopConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS=(int),
    CELERY_RETRY_ATTEMPTS=(int),
    DJANGO_CACHE_TIME=(int),
)

environ.Env.read_env(BASE_DIR.parent / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_IS_DEBUG", default=False)

ALLOWED_HOSTS = tuple(allowed_host for allowed_host in env.list("DJANGO_ALLOWED_HOSTS"))

INTERNAL_IPS = tuple(allowed_host for allowed_host in env.list("DJANGO_ALLOWED_HOSTS"))

DJANGO_SUPER_ADMIN = env("DJANGO_SUPER_ADMIN")

DJANGO_SUPER_ADMIN_PASSWORD = env("DJANGO_SUPER_ADMIN_PASSWORD")

DJANGO_SUPER_ADMIN_EMAIL = env("DJANGO_SUPER_ADMIN_EMAIL")

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "drf_yasg",
    "rest_framework",
    "django_celery_beat",
    "django_object_actions",
]
LOCAL_APPS = [
    "shop",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar", "django_extensions"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "NAME": env("DB_NAME"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AWS S3
AWS_S3_ENDPOINT_URL = env("MINIO_URL")
AWS_S3_REGION_NAME = env("MINIO_REGION_NAME")
AWS_S3_ACCESS_KEY_ID = env("MINIO_ROOT_USER")
AWS_S3_SECRET_ACCESS_KEY = env("MINIO_ROOT_PASSWORD")
AWS_STORAGE_BUCKET_NAME = env("MINIO_STATIC_BACKET_NAME")
MINIO_MEDIA_BACKET_NAME = env("MINIO_MEDIA_BACKET_NAME")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": AWS_S3_ACCESS_KEY_ID,
            "secret_key": AWS_S3_SECRET_ACCESS_KEY,
            "bucket_name": MINIO_MEDIA_BACKET_NAME,
            "endpoint_url": AWS_S3_ENDPOINT_URL,
            "region_name": AWS_S3_REGION_NAME,
            "url_protocol": "http:",
            "custom_domain": "localhost:9000/media",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        "OPTIONS": {
            "access_key": AWS_S3_ACCESS_KEY_ID,
            "secret_key": AWS_S3_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "endpoint_url": AWS_S3_ENDPOINT_URL,
            "region_name": AWS_S3_REGION_NAME,
            "url_protocol": "http:",
            "custom_domain": "localhost:9000/static",
        },
    },
}

# Cache
DJANGO_CACHE_TIME = env("DJANGO_CACHE_TIME")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("DJANGO_DEFAULT_CACHE_URL"),
    },
}

# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RETRY_ATTEMPTS = env("CELERY_RETRY_ATTEMPTS")
CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS = env("CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# Logs
if DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django.db.backends": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
        },
    }
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": "django.log",
                "formatter": "verbose",
            },
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
        },
    }

# DRF
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
}
