"""
Django settings for wesolar project.
"""

from pathlib import Path
import dj_database_url
import os
from decouple import config
from urllib.parse import urlparse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.vercel.app', '.now.sh']

if not DEBUG:
    ALLOWED_HOSTS.extend([
        'simulador-cs-back.vercel.app',  # Tu dominio específico de Vercel
        '.vercel.app',
        '*'  # Solo para desarrollo inicial, luego especifica dominios exactos
    ])

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
    'corsheaders',
    'drf_spectacular',
    # 'djoser',  # Comentado por problemas de entorno
    'rest_framework.authtoken',
]

LOCAL_APPS = [
    'authentication',
    'projects',
    'simulations',
    'core',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wesolar.urls'

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

WSGI_APPLICATION = 'wesolar.wsgi.application'

# Configuración de base de datos condicional
if config('DEVELOPMENT', default=False, cast=bool):
    # Base de datos de desarrollo (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Base de datos de producción (PostgreSQL en Neon)
    database_url = config('DATABASE_URL', default='postgresql://neondb_owner:npg_oDHPcpSE1U2b@ep-calm-surf-aek5ez53-pooler.c-2.us-east-2.aws.neon.tech:5432/neondb?sslmode=require&channel_binding=require')
    tmpPostgres = urlparse(database_url)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': tmpPostgres.path.replace('/', ''),
            'USER': tmpPostgres.username,
            'PASSWORD': tmpPostgres.password,
            'HOST': tmpPostgres.hostname,
            'PORT': tmpPostgres.port or 5432,
            'OPTIONS': {
                'sslmode': 'require',
                'channel_binding': 'require',
            }
        }
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
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration for static files (solo en producción)
if not DEBUG:
    try:
        import whitenoise
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    except ImportError:
        # Fallback si whitenoise no está disponible
        pass
else:
    # En desarrollo usar el storage por defecto
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Static files directories
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Ensure staticfiles directory exists
import os
staticfiles_dir = BASE_DIR / 'staticfiles'
if not staticfiles_dir.exists():
    staticfiles_dir.mkdir(parents=True, exist_ok=True)

MEDIA_URL = '/media/'
if DEBUG:
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    # En producción usar servicio externo para media files
    MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model (comentado temporalmente)
# AUTH_USER_MODEL = 'authentication.User'

# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# CORS settings for React frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000",
    "https://simulador-cs-front.vercel.app",  # Producción frontend
]

# Permitir todos los orígenes en desarrollo
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

# API Documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'WeSolar API',
    'DESCRIPTION': 'API para simulación de inversiones en proyectos solares comunitarios',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Email configuration
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='WeSolar <no-reply@wesolar.com>')

# Djoser configuration (comentado temporalmente)
# DJOSER = {
#     'LOGIN_FIELD': 'username',  # Usar username por ahora con el User por defecto
#     'USER_CREATE_PASSWORD_RETYPE': True,
#     'USERNAME_CHANGED_EMAIL_CONFIRMATION': False,  # Deshabilitado para User por defecto
#     'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
#     'SEND_CONFIRMATION_EMAIL': True,
#     'SEND_ACTIVATION_EMAIL': True,
#     'SET_PASSWORD_RETYPE': True,
#     'PASSWORD_RESET_CONFIRM_RETYPE': True,
#     'TOKEN_MODEL': None,  # Use built-in Token model
#     'ACTIVATION_URL': config('FRONTEND_ACTIVATION_URL', default='http://localhost:3000/activate') + '/{uid}/{token}',
#     'PASSWORD_RESET_CONFIRM_URL': config('FRONTEND_PASSWORD_RESET_URL', default='http://localhost:3000/reset-password') + '/{uid}/{token}',
#     'SERIALIZERS': {
#         'user_create': 'authentication.serializers.UserCreateSerializer',
#         'user': 'authentication.serializers.UserSerializer',
#         'current_user': 'authentication.serializers.UserSerializer',
#     },
#     'EMAIL': {
#         'activation': 'authentication.email.ActivationEmail',
#         'confirmation': 'authentication.email.ConfirmationEmail',
#         'password_reset': 'authentication.email.PasswordResetEmail',
#     },
#     'PERMISSIONS': {
#         'user': ['djoser.permissions.CurrentUserOrAdmin'],
#         'user_list': ['rest_framework.permissions.IsAdminUser'],
#     },
# }

# Frontend URLs for email templates
FRONTEND_ACTIVATION_URL = config('FRONTEND_ACTIVATION_URL', default='http://localhost:3000/activate')
FRONTEND_PASSWORD_RESET_URL = config('FRONTEND_PASSWORD_RESET_URL', default='http://localhost:3000/reset-password')