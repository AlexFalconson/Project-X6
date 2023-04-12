import environ as django_environ

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from pathlib import Path

env = django_environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('APP_SECRET_KEY', default='d283cf4fb4ca8b1aeec08a5eaa8f0bb4')

DEBUG = env.bool('APP_DEBUG', default=False)

ALLOWED_HOSTS = env.list('APP_ALLOWED_HOSTS', default=['*'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'drf_spectacular',

    # own
    'api.user',
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

AUTH_USER_MODEL = 'user.User'

TEST_RUNNER = 'core.utils.CustomTestRunner'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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


# Feature vars

FEATURE_SWAGGER = env.bool('APP_FEATURE_SWAGGER', default=True)


# Database

DATABASES = {
    'default': env.db('APP_DB_URL', default='postgres://localhost', engine='django.db.backends.postgresql'),
}
DATABASES['default']['CONN_MAX_AGE'] = 60 * 5  # for persistent db connections


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


# REST API

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')

SPECTACULAR_SETTINGS = {
    'TITLE': 'Template API',
    'VERSION': 'v1',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'GET_MOCK_REQUEST': 'core.utils.build_swagger_mock_request',
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'displayRequestDuration': True,
        'persistAuthorization': True,
    },
}


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] [{levelname}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# Fixtures

FIXTURE_DIRS = BASE_DIR / 'fixtures',


# Internationalization

LOCALE_PATHS = BASE_DIR / 'locales',

LANGUAGES = (
    ('en', _('English')),
    ('uk', _('Ukrainian')),
)

LANGUAGE_CODE = env('APP_DEFAULT_LANG', default='en')
if LANGUAGE_CODE not in (lang[0] for lang in LANGUAGES):
    raise ImproperlyConfigured(f'Specified default language not supported: {LANGUAGE_CODE}')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
