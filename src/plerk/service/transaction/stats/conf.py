from os import environ
from warnings import warn

ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "*").split(",")

AUTH_PASSWORD_VALIDATORS = []

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "plerk.service.transaction.stats",
  }
}

DEBUG = environ.get("DEBUG", "no") == "on"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
  "rest_framework",
  "plerk.service.transaction.stats.apps.AppConfig",
]

LOGGING = {
  "version": 1,
  "formatters": {
    "prettysql": {
      "()": "plerk.service.transaction.stats.util.PrettySQL",
      "format": "\n\n%(prettysql)s(%(duration).3f)\n\n",
    }
  },
  "handlers": {
    "prettysql": {
      "class": "logging.StreamHandler",
      "filters": [],
      "formatter": "prettysql",
    }
  },
  "loggers": {
    "django.db.backends": {
      "handlers": ["prettysql"],
      "level": "NOTSET",
    }
  }
}

MIDDLEWARE = [
  "django.middleware.security.SecurityMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "plerk.service.transaction.stats.urls"

SECRET_KEY = "django-insecure-bz_(uuk^&#5c6yf8nk!y^hyi5lmkg11m_-2hyuow8wafamii^$"

REST_FRAMEWORK = {
  "DEFAULT_AUTHENTICATION_CLASSES": [],
  "DEFAULT_PERMISSION_CLASSES": [],
  "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
  "UNAUTHENTICATED_USER": None,
}

TEMPLATES = []

TIME_ZONE = "America/Guayaquil"

USE_I18N = False

USE_TZ = True

WSGI_APPLICATION = "plerk.service.transaction.stats.wsgi.application"

if environ.get("DEBUG_LOGGING_SQL", "no") == "on":
  if not DEBUG:
    warn("DEBUG is required for DEBUG_LOGGING_SQL to work")
  LOGGING["loggers"]["django.db.backends"]["level"] = "DEBUG"
