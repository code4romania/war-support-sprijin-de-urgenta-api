from revm_site.settings.base import *

DEBUG: bool = False

SECRET_KEY: str = env.str("SECRET_KEY")

EMAIL_BACKEND: str = "django_q_email.backends.DjangoQBackend"

ALLOWED_HOSTS: List[str] = ALLOWED_HOSTS or ["*"]
