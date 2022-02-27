"""
Django settings for revm_site project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os

import environ
from django.utils.translation import gettext_lazy as _

env = environ.Env(
    # set casting, default value
    ENVIRONMENT=(str, "production"),
    ENABLE_DEBUG_TOOLBAR=(bool, True),
    LANGUAGE_CODE=(str, "en"),
    HOME_SITE_URL=(str, ""),
    ALLOWED_HOSTS=(list, ["*"]),
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")

DEBUG = env("ENVIRONMENT") != "production"

ENABLE_DEBUG_TOOLBAR = bool(DEBUG and env("ENABLE_DEBUG_TOOLBAR"))

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CORS_ORIGIN_ALLOW_ALL = False

INSTALLED_APPS = [
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "django.contrib.postgres",
    # third-party apps
    "rest_framework",
    "storages",
    "corsheaders",
    # project apps
    "donors",
    "available_resources",
    # api documentation
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SITE_ID = 1

ROOT_URLCONF = "revm_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "revm_site.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = env("LANGUAGE_CODE")
TIME_ZONE = "Europe/Bucharest"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ("ro", _("Romanian")),
    ("en", _("English")),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

PRIVATE_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "./public/media")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "VERSION": "0.1.0",
    "SWAGGER_UI_SETTINGS": {"url": "/api/v1/schema"},
}

COUNTIES_SHORTNAME = {
    "AB": "Alba",
    "AR": "Arad",
    "AG": "Argeș",
    "BC": "Bacău",
    "BH": "Bihor",
    "BN": "Bistrița-Năsăud",
    "BT": "Botoșani",
    "BV": "Brașov",
    "BR": "Brăila",
    "B": "București",
    "BZ": "Buzău",
    "CL": "Călărași",
    "CS": "Caraș-Severin",
    "CJ": "Cluj",
    "CT": "Constanța",
    "CV": "Covasna",
    "DB": "Dâmbovița",
    "DJ": "Dolj",
    "GL": "Galați",
    "GR": "Giurgiu",
    "GJ": "Gorj",
    "HR": "Harghita",
    "HD": "Hunedoara",
    "IL": "Ialomița",
    "IS": "Iași",
    "IF": "Ilfov",
    "MM": "Maramureș",
    "MH": "Mehedinți",
    "MS": "Mureș",
    "NT": "Neamț",
    "OT": "Olt",
    "PH": "Prahova",
    "SM": "Satu Mare",
    "SJ": "Sălaj",
    "SB": "Sibiu",
    "SV": "Suceava",
    "TR": "Teleorman",
    "TM": "Timiș",
    "TL": "Tulcea",
    "VS": "Vaslui",
    "VL": "Vâlcea",
    "VN": "Vrancea",
    "RO": "Național",
}
