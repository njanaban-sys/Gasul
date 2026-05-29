import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ──────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-gasul-lpg-surigao-dev-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

# ── Apps ──────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'products',
    'orders',
    'dashboard',
]

# ── Middleware ────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gasul_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'gasul_project.wsgi.application'

# ── Database ──────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.environ.get('DB_NAME',     'postgres'),
        'USER':     os.environ.get('DB_USER',     'postgres.vewzjqzihrbzuxjcawyc'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'Dadar#27032006'),
        'HOST':     os.environ.get('DB_HOST',     'aws-1-ap-southeast-2.pooler.supabase.com'),
        'PORT':     os.environ.get('DB_PORT',     '6543'),
        'OPTIONS': {
            'sslmode': 'require',
        },
        'CONN_MAX_AGE': 60,
    }
}

# ── Auth ──────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# ── Localisation ──────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Manila'
USE_I18N      = True
USE_TZ        = True

# ── Static & Media ────────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = '/tmp/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL             = '/users/login/'
LOGIN_REDIRECT_URL    = '/'
LOGOUT_REDIRECT_URL   = '/users/login/'

# ── CSRF — trust ALL vercel.app subdomains ────────────────────────
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.njanaban-sys-projects.vercel.app',
]
