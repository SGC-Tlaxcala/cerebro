from unipath import Path
import environ
from django.contrib.messages import constants as messages
import datetime
try:
    import locale
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
except Exception:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except Exception as e:
        messages.error(request, 'An error occurred: {0}'.format(e))

VERSION = '1.7.0'

BASE_DIR = Path(__file__).ancestor(2)
APPS_DIR = BASE_DIR.child('apps')
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(BASE_DIR.child('.env'))

SECRET_KEY = env('SECRET_KEY', default='5kho_evo8b7font)yy(^p!1w$skj%)#5yw-097cr@=%w=8#i7z')

DEBUG = env("DEBUG", default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default='*')
if env('SSL', default=False) is True:
    SECURE_SSL_REDIRECT = False

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize'
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'crispy_forms',
    'django_extensions',
    'watson',
    'debug_toolbar',
    'simple_history'
]
LOCAL_APPS = [
    'core',
    'apps.profiles.config.ProfilesConfig',
    'apps.docs.config.DocsConfig',
    'apps.mesas.config.MesasConfig',
    'apps.paquetes.config.PaquetesConfig',
    'apps.productividad.config.ProductividadConfig',
    'apps.dpi.config.DpiConfig',
    'apps.cecyrd.config.CecyrdConfig'
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            APPS_DIR.child('templates'),
            'templates'
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

DATABASES = {
    'default': env.db()
}

if DEBUG:
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        }
    ]
else:
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


LANGUAGE_CODE = env('LOCALE', default='es-mx')
TIME_ZONE = 'Mexico/General'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1

LOGIN_REDIRECT_URL = '/'

STATIC_ROOT = APPS_DIR.child('assets')
STATIC_URL = '/assets/'
STATICFILES_DIRS = [
    APPS_DIR.child('static')
]

MEDIA_ROOT = APPS_DIR.child('media')
MEDIA_URL = '/media/'
FILE_UPLOAD_PERMISSIONS = 0o644

CRISPY_TEMPLATE_PACK = 'bootstrap4'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),  # 3 days
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=60),  # 3 days
    'JWT_AUTH_COOKIE': 'JWT',
    'JWT_ALLOW_REFRESH': True
}

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',  # message level to be written to console
        },
    },
    'loggers': {
        '': {
            # this sets root level logger to log debug and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,    # this tells logger to send logging message
                                   # to its parent (will send if set to True)
        },
        # 'django.db': {
        #     # django also has database level logging
        #     'level': 'DEBUG'
        # },
    },
}

INTERNAL_IPS = '127.0.0.1'
