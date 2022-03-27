from revm_site.settings.base import *

DEBUG: bool = True

SECRET_KEY: str = env.str("SECRET_KEY")

EMAIL_BACKEND: str = "django_q_email.backends.DjangoQBackend"

ALLOWED_HOSTS: List[str] = ALLOWED_HOSTS or ["*"]
CORS_ALLOW_ALL_ORIGINS: bool = True

if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    def show_toolbar(_):
        return True

    DEBUG_TOOLBAR_CONFIG: Dict[str, callable] = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }
