from pathlib import Path
import os
from dotenv import load_dotenv
from django.contrib.messages import constants

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')



SECRET_KEY = 'django-insecure-)o62#v++_ole3f+wbdp-v=_m8u=zbqyv3olyepfu_htv(k4yh7'

DEBUG = True

ALLOWED_HOSTS = []

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'plataforma',
    'tailwind',
    'theme',
     'django_browser_reload'
]
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = "/usr/local/bin/npm"
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     "django_browser_reload.middleware.BrowserReloadMiddleware",

]

ROOT_URLCONF = 'enginer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'plataforma.context_processors.empresa',
            ],
        },
    },
]

WSGI_APPLICATION = 'enginer.wsgi.application'



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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DB_NAME'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST', default='localhost'),
        'PORT': os.getenv('MYSQL_PORT', default='3306'),
    }
}

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_TZ = False 

USE_I18N = True


AUTH_USER_MODEL = 'login.Pessoa'


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates', 'static'),
    os.path.join(BASE_DIR, 'theme', 'static_src', 'node_modules', 'flowbite'),
    os.path.join(BASE_DIR, 'theme', 'static_src', 'node_modules', 'flowbite-typography'),
    os.path.join(BASE_DIR, 'theme', 'static_src', 'node_modules', '@tiptap'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
NPM_BIN_PATH = 'C:/Program Files/nodejs/npm.cmd'

#Django Message

MESSAGE_TAGS = {
    constants.DEBUG: 'bg-gray-100 text-gray-800 border-gray-300',
    constants.INFO: 'bg-blue-100 text-blue-800 border-blue-300',
    constants.SUCCESS: 'bg-green-100 text-green-800 border-green-300',
    constants.WARNING: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    constants.ERROR: 'bg-red-100 text-red-800 border-red-300',
}