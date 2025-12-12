import os
from pathlib import Path

# ---------------- BASE ----------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'changeme-for-dev'  # change for production
DEBUG = True  # True for local development
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ---------------- INSTALLED APPS ----------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tailwind',
    'theme',
    'django_browser_reload',

    'crispy_forms',

    'shop',
]

TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

# ---------------- MIDDLEWARE ----------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------- URL & WSGI ----------------
ROOT_URLCONF = 'ecommerce_site.urls'
WSGI_APPLICATION = 'ecommerce_site.wsgi.application'

# ---------------- DATABASE ----------------
# Local development: use SQLite (no MySQL/PostgreSQL needed)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For production with MySQL/PostgreSQL, uncomment and configure:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # or 'django.db.backends.postgresql'
#         'NAME': 'ecommerce_db',
#         'USER': 'root',
#         'PASSWORD': 'Srinu@123',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# ---------------- TEMPLATES ----------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # global templates folder
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

# ---------------- PASSWORD VALIDATION ----------------
AUTH_PASSWORD_VALIDATORS = []

# ---------------- INTERNATIONALIZATION ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ---------------- STATIC & MEDIA ----------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------- OTHER ----------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'
