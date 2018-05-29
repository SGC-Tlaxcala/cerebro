from unipath import Path
from json_environ import Environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).ancestor(2)
env_path = BASE_DIR.child('.env.json')
env = Environ(path=env_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='5kho_evo8b7font)yy(^p!1w$skj%)#5yw-097cr@=%w=8#i7z')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=True)
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
if env('SSL', default=False) is True:
    SECURE_SSL_REDIRECT = False

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'crispy_forms'
]
LOCAL_APPS = [
    'profiles',
    'metas',
    'dpi.apps.DpiConfig'
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
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates')],
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
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{env("DATABASE:ENGINE", default="sqlite")}',
        'NAME': env("DATABASE:NAME"),
        'USER': env("DATABASE:USER"),
        'PASSWORD': env("DATABASE:PASSWORD")
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'Mexico/General'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1

STATIC_ROOT = BASE_DIR.child('assets')
STATIC_URL = '/assets/'
STATICFILES_DIRS = (
    str(BASE_DIR.child('static')),
)

MEDIA_ROOT = BASE_DIR.child('media')
MEDIA_URL = '/media/'

# CRISPY FORMS SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}
