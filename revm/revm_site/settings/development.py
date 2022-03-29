import os
from typing import List

from revm_site.settings.base import *

DEBUG: bool = True
ALLOWED_HOSTS: List[str] = ["*"]
CORS_ALLOW_ALL_ORIGINS: bool = True
SECRET_KEY: str = "secret"

if env("DEV_ENABLE_EMAIL_SMTP") == "yes":
    EMAIL_BACKEND: str = "django_q_email.backends.DjangoQBackend"
else:
    EMAIL_BACKEND: str = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS.insert(0, "django_extensions")
INSTALLED_APPS.insert(0, "whitenoise.runserver_nostatic")

if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    def show_toolbar(_):
        return True

    DEBUG_TOOLBAR_CONFIG: Dict[str, callable] = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }
