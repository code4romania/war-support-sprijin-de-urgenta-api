from revm_site.settings.base import *

DEBUG = TEMPLATE_DEBUG = False

SECRET_KEY = env.str("SECRET_KEY")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = []
