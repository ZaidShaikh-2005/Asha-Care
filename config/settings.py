"""
Django settings for config project.

ASHA Care Desktop Application
"""

from pathlib import Path
import sys


# =========================================================
# PATH CONFIGURATION
# =========================================================

if getattr(sys, "frozen", False):
    # PyInstaller temporary resource directory.
    # Contains bundled templates/static/staticfiles/config/core.
    BASE_DIR = Path(sys._MEIPASS)

    # Folder containing AshaNurseApp.exe.
    # Database and media will be stored here.
    APP_DIR = Path(sys.executable).resolve().parent

else:
    # Normal development mode.
    BASE_DIR = Path(__file__).resolve().parent.parent
    APP_DIR = BASE_DIR


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = 'django-insecure-w@#_824owcmr(23tz&2znz+2xf+_*!2+rpvx+8#-llavc63yjl'

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Serve static files when running through Waitress/PyInstaller.
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================================================
# URL CONFIGURATION
# =========================================================

ROOT_URLCONF = 'config.urls'


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates',
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = 'config.wsgi.application'


# =========================================================
# DATABASE
# =========================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',

        # Development:
        # asha_nurse_app/db.sqlite3
        #
        # PyInstaller:
        # dist/AshaNurseApp/db.sqlite3
        'NAME': APP_DIR / 'db.sqlite3',
    }
}


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = '/static/'

# Original project static files.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# collectstatic copies all CSS/JS/images here.
STATIC_ROOT = BASE_DIR / 'staticfiles'


# =========================================================
# STATIC FILE STORAGE
# =========================================================

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# =========================================================
# WHITENOISE
# =========================================================

WHITENOISE_USE_FINDERS = True

WHITENOISE_AUTOREFRESH = True


# =========================================================
# MEDIA FILES
# =========================================================

MEDIA_URL = '/media/'

# Development:
# asha_nurse_app/media/
#
# PyInstaller:
# dist/AshaNurseApp/media/
MEDIA_ROOT = APP_DIR / 'media'


# =========================================================
# EMAIL SETTINGS
# =========================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'ashaanursing2026@gmail.com'

# IMPORTANT:
# Generate a NEW Gmail App Password.
# Do not use the previously exposed password.
EMAIL_HOST_PASSWORD = 'lzutpiyftzovxlhx'

DEFAULT_FROM_EMAIL = 'ashaanursing2026@gmail.com'


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'