"""
Django settings for website project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in ('1', 'true', 'yes', 'on')


DEBUG = env_bool('DEBUG', True)

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-2t)cq^reuyyw7ds_7i0s885!6&0qd=8!))i)0i)j)=w311k!&$',
)

_allowed_hosts = os.environ.get('ALLOWED_HOSTS')
if _allowed_hosts:
    ALLOWED_HOSTS = [host.strip() for host in _allowed_hosts.split(',') if host.strip()]
elif DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'home',
    'accounts',
    'cart',
    'order',
    'ckeditor',
    'ckeditor_uploader',
    'taggit',
    'django_filters',
    'phone_field',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'home.context_processors.electro_layout',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=env_bool('DATABASE_SSL_REQUIRE', False),
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': os.environ.get('DB_NAME', 'home_appliances_db'),
            'USER': os.environ.get('DB_USER', 'ebi'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'aA1aA1aA1'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'OPTIONS': {
                'driver': os.environ.get('DB_DRIVER', 'ODBC Driver 17 for SQL Server'),
                'extra_params': 'TrustServerCertificate=yes',
            },
        }
    }

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('de', 'Deutsch'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

if not DEBUG:
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
        },
    }

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Basic',
        'height': 300,
        'width': '100%',
    },
}

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'home:home'
LOGOUT_REDIRECT_URL = 'home:home'

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend',
)

SITE_URL = os.environ.get('SITE_URL', 'http://127.0.0.1:8001').rstrip('/')

ZARINPAL_MERCHANT_ID = os.environ.get(
    'ZARINPAL_MERCHANT_ID',
    'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
)
ZARINPAL_SANDBOX = env_bool('ZARINPAL_SANDBOX', True)
ZARINPAL_CALLBACK_URL = os.environ.get(
    'ZARINPAL_CALLBACK_URL',
    f'{SITE_URL}/order/payment/callback/',
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

JAZZMIN_SETTINGS = {
    'site_title': 'Home Appliances Admin',
    'site_header': 'Home Appliances',
    'site_brand': 'Home Appliances',
    'welcome_sign': 'Welcome to Home Appliances Store',
    'copyright': 'Home Appliances Store',
    'search_model': 'home.Product',
    'topmenu_links': [
        {'name': 'Storefront', 'url': '/', 'new_window': True},
    ],
    'icons': {
        'accounts.User': 'fas fa-user',
        'accounts.EmailToken': 'fas fa-envelope',
        'home.Product': 'fas fa-blender',
        'home.Category': 'fas fa-folder',
        'home.Brand': 'fas fa-tag',
        'home.Comment': 'fas fa-comment',
        'cart.Cart': 'fas fa-shopping-cart',
        'order.Order': 'fas fa-receipt',
        'order.Coupon': 'fas fa-ticket-alt',
    },
}

JAZZMIN_UI_TWEAKS = {
    'theme': 'flatly',
    'navbar': 'navbar-dark navbar-primary',
    'sidebar': 'sidebar-dark-primary',
}
