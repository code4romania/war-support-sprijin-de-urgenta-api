import os

from revm_site.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True
SECRET_KEY = "secret"
if env("DEV_ENABLE_EMAIL_SMTP") == "yes":
    EMAIL_BACKEND = "django_q_email.backends.DjangoQBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = ["whitenoise.runserver_nostatic", "django_extensions"] + INSTALLED_APPS

if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

    def show_toolbar(_):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }
