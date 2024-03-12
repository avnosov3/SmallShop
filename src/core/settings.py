from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

environ.Env.read_env(BASE_DIR.parent / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_IS_DEBUG", default=False)

ALLOWED_HOSTS = tuple(allowed_host for allowed_host in env.list('DJANGO_ALLOWED_HOSTS'))

# Application definition
INSTALLED_APPS = [
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

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'NAME': env('DB_NAME'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    },
}

# Password validation
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
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AWS S3
AWS_S3_ENDPOINT_URL = env('MINIO_URL')
AWS_S3_REGION_NAME = env('MINIO_REGION_NAME')
AWS_S3_ACCESS_KEY_ID = env('MINIO_ROOT_USER')
AWS_S3_SECRET_ACCESS_KEY = env('MINIO_ROOT_PASSWORD')
AWS_STORAGE_BUCKET_NAME = env('MINIO_MEDIA_BACKET_NAME')
MINIO_STATIC_BACKET_NAME = env('MINIO_STATIC_BACKET_NAME')

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {
            'access_key': AWS_S3_ACCESS_KEY_ID,
            'secret_key': AWS_S3_SECRET_ACCESS_KEY,
            'bucket_name': AWS_STORAGE_BUCKET_NAME,
            'endpoint_url': AWS_S3_ENDPOINT_URL,
            'region_name': AWS_S3_REGION_NAME,
        },
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.s3boto3.S3StaticStorage',
        'OPTIONS': {
            'access_key': AWS_S3_ACCESS_KEY_ID,
            'secret_key': AWS_S3_SECRET_ACCESS_KEY,
            'bucket_name': MINIO_STATIC_BACKET_NAME,
            'endpoint_url': AWS_S3_ENDPOINT_URL,
            'region_name': AWS_S3_REGION_NAME,
        },
    },
}
