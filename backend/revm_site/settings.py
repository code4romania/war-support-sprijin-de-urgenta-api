"""
Django settings for revm_site project.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from copy import deepcopy
from datetime import timedelta

import environ
import sentry_sdk
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

env = environ.Env(
    # set casting, default value
    ENVIRONMENT=(str, "production"),
    DEBUG=(bool, False),
    ENABLE_DEBUG_TOOLBAR=(bool, False),
    DEV_ENABLE_EMAIL_SMTP=(bool, False),
    ENABLE_DUMP_LOCAL_SAVE=(bool, False),
    LANGUAGE_CODE=(str, "en"),
    HOME_SITE_URL=(str, ""),
    ALLOWED_HOSTS=(list, ["*"]),
    IS_CONTAINERIZED=(bool, False),
    # Error logging
    ## Through Slack
    ENABLE_SLACK_LOGGING=(bool, True),
    SLACK_WEBHOOK_URL=(str, ""),
    SLACK_LOGGING_COLOR=(str, ""),
    ## Through Sentry
    SENTRY_DSN=(str, ""),
    # Email settings
    FROM_EMAIL=(str, "noreply@code4.ro"),
    EMAIL_HOST=(str, ""),
    EMAIL_PORT=(str, ""),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_USE_TLS=(bool, True),
    EMAIL_USE_SSL=(bool, False),
    # S3
    USE_S3=(bool, False),
    AWS_S3_REGION_NAME=(str, ""),
    AWS_S3_SIGNATURE_VERSION=(str, "s3v4"),
    AWS_S3_ADDRESSING_STYLE=(str, "virtual"),
    AWS_S3_STORAGE_DEFAULT_BUCKET_NAME=(str, ""),
    AWS_S3_STORAGE_PUBLIC_BUCKET_NAME=(str, ""),
    AWS_S3_STORAGE_STATIC_BUCKET_NAME=(str, ""),
    AWS_S3_DEFAULT_ACL=(str, "private"),
    AWS_S3_PUBLIC_ACL=(str, ""),
    AWS_S3_STATIC_ACL=(str, ""),
    AWS_S3_DEFAULT_PREFIX=(str, ""),
    AWS_S3_PUBLIC_PREFIX=(str, ""),
    AWS_S3_STATIC_PREFIX=(str, ""),
    AWS_S3_DEFAULT_CUSTOM_DOMAIN=(str, ""),
    AWS_S3_PUBLIC_CUSTOM_DOMAIN=(str, ""),
    AWS_S3_STATIC_CUSTOM_DOMAIN=(str, ""),
    # SES
    AWS_SES_REGION_NAME=(str, ""),
    AWS_SES_USE_V2=(bool, True),
    AWS_SES_CONFIGURATION_SET_NAME=(str, None),
    AWS_SES_AUTO_THROTTLE=(float, 0.5),
    AWS_SES_REGION_ENDPOINT=(str, ""),
)

ENABLE_DUMP_LOCAL_SAVE = env.bool("ENABLE_DUMP_LOCAL_SAVE")

ADMIN_TITLE = _("Sprijin de Urgență")
ADMIN_TITLE_SHORT = _("SDU")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir)

SECRET_KEY = env.str("SECRET_KEY")

ENVIRONMENT = env("ENVIRONMENT")
DEBUG = bool(ENVIRONMENT == "development") and env.bool("DEBUG")
ENABLE_DEBUG_TOOLBAR = DEBUG and env.bool("ENABLE_DEBUG_TOOLBAR")

# Application definition
APPEND_SLASH = True

# some settings will be different if it's not running in a container (e.g., locally, on a Mac)
IS_CONTAINERIZED = env.bool("IS_CONTAINERIZED")

DEFAULT_REVISION_STRING = "dev"

VERSION = env.str("VERSION", "edge")
REVISION = env.str("REVISION", DEFAULT_REVISION_STRING)
REVISION = REVISION[:7]

if IS_CONTAINERIZED and VERSION == "edge" and REVISION == DEFAULT_REVISION_STRING:
    version_file = "/var/www/redirect/.version"
    if os.path.exists(version_file):
        with open(version_file) as f:
            VERSION, REVISION = f.read().strip().split("+")

VERSION_SUFFIX = f"{VERSION}+{REVISION}"
VERSION_LABEL = f"redirect@{VERSION_SUFFIX}"

# Error Logging
ENABLE_SLACK_LOGGING = env.bool("ENABLE_SLACK_LOGGING")
if ENABLE_SLACK_LOGGING:
    SLACK_WEBHOOK_URL = env("SLACK_WEBHOOK_URL")
    SLACK_LOGGING_COLOR = env("SLACK_LOGGING_COLOR")

# Sentry
ENABLE_SENTRY = True if env.str("SENTRY_DSN") else False
if ENABLE_SENTRY:
    sentry_sdk.init(
        dsn=env.str("SENTRY_DSN"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE"),
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=env.float("SENTRY_PROFILES_SAMPLE_RATE"),
        environment=ENVIRONMENT,
        release=VERSION_LABEL,
    )

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
        "slack": {
            "level": "ERROR",
            "class": "revm_site.handlers.SlackHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["slack", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    "unfold",
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
    "impersonate",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "storages",
    "corsheaders",
    "dj_rest_auth",
    "import_export",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "django_q",
    "multiselectfield",
    "crispy_forms",
    "crispy_tailwind",
    # project apps
    "static_custom",
    "app_account",
    "app_item",
    "app_transport_service",
    "app_volunteering",
    "app_other",
    "app_food_request",
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
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "impersonate.middleware.ImpersonateMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "revm_site.middlewares.AdminErrorMiddleware.AdminErrorMiddleware",
]

if ENVIRONMENT == "development":
    INSTALLED_APPS = [
        "whitenoise.runserver_nostatic",
        "django_extensions",
    ] + INSTALLED_APPS

if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

    def show_toolbar(_):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }

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

# Impersonation settings
# https://pypi.org/project/django-impersonate/

IMPERSONATE = {
    "REDIRECT_URL": "/admin/",
    "REQUIRE_SUPERUSER": True,
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
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
USE_TZ = True

LANGUAGES = [
    ("ro", _("Romanian")),
    ("en", _("English")),
    ("es", _("Spanish")),
    ("uk", _("Ukrainian")),
    ("ru", _("Russian")),
]

# Media & Static files storage
# https://docs.djangoproject.com/en/4.2/howto/static-files/

static_static_location = "static"
public_media_location = "media"
private_media_location = "media"

static_storage = "whitenoise.storage.CompressedStaticFilesStorage"
media_storage = "django.core.files.storage.FileSystemStorage"

STATIC_URL = f"{static_static_location}/"
MEDIA_URL = f"{public_media_location}/"

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "static"))
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "media"))

STATICFILES_DIRS = [
    os.path.abspath(os.path.join("static_custom")),
]

default_storage_options = {}

public_storage_options = {}
static_storage_options = {}

if env.bool("USE_S3"):
    media_storage = "storages.backends.s3boto3.S3Boto3Storage"
    static_storage = "storages.backends.s3boto3.S3StaticStorage"

    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
    default_storage_options = {
        "bucket_name": env.str("AWS_S3_STORAGE_DEFAULT_BUCKET_NAME"),
        "default_acl": env.str("AWS_S3_DEFAULT_ACL"),
        "region_name": env.str("AWS_S3_REGION_NAME") or env.str("AWS_REGION_NAME"),
        "object_parameters": {"CacheControl": "max-age=86400"},
        "file_overwrite": False,
        "signature_version": env.str("AWS_S3_SIGNATURE_VERSION"),
        "addressing_style": env.str("AWS_S3_ADDRESSING_STYLE"),
    }

    # Authentication, if not using IAM roles
    if aws_session_profile := env.str("AWS_S3_SESSION_PROFILE", default=None):
        default_storage_options["session_profile"] = aws_session_profile
    elif aws_access_key := env.str("AWS_ACCESS_KEY_ID", default=None):
        default_storage_options["access_key"] = aws_access_key
        default_storage_options["secret_key"] = env.str("AWS_SECRET_ACCESS_KEY")

    # Additional default configurations
    if default_prefix := env.str("AWS_S3_DEFAULT_PREFIX", default=None):
        default_storage_options["location"] = default_prefix
    if custom_domain := env.str("AWS_S3_DEFAULT_CUSTOM_DOMAIN", default=None):
        public_storage_options["custom_domain"] = custom_domain

    # Public storage options
    public_storage_options = deepcopy(default_storage_options)
    if public_acl := env.str("AWS_S3_PUBLIC_ACL"):
        public_storage_options["default_acl"] = public_acl
    if public_bucket_name := env.str("AWS_S3_STORAGE_PUBLIC_BUCKET_NAME"):
        public_storage_options["bucket_name"] = public_bucket_name
    if public_prefix := env.str("AWS_S3_PUBLIC_PREFIX", default=None):
        public_storage_options["location"] = public_prefix
    if custom_domain := env.str("AWS_S3_PUBLIC_CUSTOM_DOMAIN", default=None):
        public_storage_options["custom_domain"] = custom_domain

    static_storage_options = deepcopy(public_storage_options)
    if static_acl := env.str("AWS_S3_STATIC_ACL"):
        static_storage_options["default_acl"] = static_acl
    if static_bucket_name := env.str("AWS_S3_STORAGE_STATIC_BUCKET_NAME"):
        static_storage_options["bucket_name"] = static_bucket_name
    if static_prefix := env.str("AWS_S3_STATIC_PREFIX", default=None):
        static_storage_options["location"] = static_prefix
    if custom_domain := env.str("AWS_S3_STATIC_CUSTOM_DOMAIN", default=None):
        static_storage_options["custom_domain"] = custom_domain


STORAGES = {
    "default": {
        "BACKEND": media_storage,
        "LOCATION": private_media_location,
        "OPTIONS": default_storage_options,
    },
    "public": {
        "BACKEND": media_storage,
        "LOCATION": public_media_location,
        "OPTIONS": public_storage_options,
    },
    "staticfiles": {
        "BACKEND": static_storage,
        "LOCATION": static_static_location,
        "OPTIONS": static_storage_options,
    },
}

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "VERSION": "1.0.0",
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
}

ITEM_STATUS_NOT_VERIFIED = "NV"
ITEM_STATUS_VERIFIED = "V"
ITEM_STATUS_DEACTIVATED = "D"
ITEM_STATUS_COMPLETE = "C"

OFFER_STATUS = (
    (ITEM_STATUS_NOT_VERIFIED, _("Not Verified")),
    (ITEM_STATUS_VERIFIED, _("Verified")),
    (ITEM_STATUS_DEACTIVATED, _("Deactivated")),
    (ITEM_STATUS_COMPLETE, _("Complete")),
)

REQUEST_STATUS = (
    (ITEM_STATUS_NOT_VERIFIED, _("Not Verified")),
    (ITEM_STATUS_VERIFIED, _("Verified")),
    (ITEM_STATUS_DEACTIVATED, _("Deactivated")),
    (ITEM_STATUS_COMPLETE, _("Solved")),
)

STATUS_COLOR_MAPPING = {
    ITEM_STATUS_DEACTIVATED: "secondary",
    ITEM_STATUS_NOT_VERIFIED: "danger",
    ITEM_STATUS_VERIFIED: "primary",
    ITEM_STATUS_COMPLETE: "success",
}

TRANSPORT_TYPES_CHOICES = ((1, _("National")), (2, _("County")))

TRANSPORT_AVAILABILTY = (
    ("WK", _("Disponibil in weekend")),
    ("WD", _("Disponibil in timpul saptamanii")),
    ("A", _("Disponibil oricand")),
    ("FI", _("Intervale fixe")),
)

COUNTY_CHOICES = list(COUNTIES_SHORTNAME.items())

PAGE_SIZE = 20

AUTH_USER_MODEL = "app_account.CustomUser"
# LOGIN_REDIRECT_URL = "admin"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

REST_USE_JWT = True
JWT_AUTH_COOKIE = "sdu-auth-cookie"
JWT_AUTH_REFRESH_COOKIE = "sdu-refresh-token"

# DRF-simplejwt https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
}

IMPORT_EXPORT_USE_TRANSACTIONS = True

# Email settings
if env.bool("DEV_ENABLE_EMAIL_SMTP") or ENVIRONMENT not in ("development", "test"):
    # XXX: change this
    EMAIL_BACKEND = "django_ses.SESBackend"
elif ENVIRONMENT == "test":
    EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

FROM_EMAIL = env("FROM_EMAIL")

EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
if not EMAIL_USE_TLS:
    EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")

SUPER_ADMIN_PASS = env("SUPER_ADMIN_PASS")
SUPER_ADMIN_EMAIL = env("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_FIRST_NAME = env("SUPER_ADMIN_FIRST_NAME")
SUPER_ADMIN_LAST_NAME = env("SUPER_ADMIN_LAST_NAME")

REST_AUTH_REGISTER_SERIALIZERS = {"REGISTER_SERIALIZER": "app_account.serializers.RegisterSerializer"}


# django-q https://django-q.readthedocs.io/en/latest/configure.html

Q_CLUSTER = {
    "name": "SdU",
    "recycle": 500,
    "timeout": 60,
    "compress": True,
    "save_limit": 250,
    "queue_limit": 500,
    "cpu_affinity": 1,
    "label": "Django Q",
    "orm": "default",
}


# django-cripsy-forms
# -------------------------------------------------------------------------------
# django-cripsy-forms - https://django-crispy-forms.readthedocs.io/en/latest/
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"


# Unfold Admin settings
# -------------------------------------------------------------------------------
# django-unfold - https://unfoldadmin.com/docs/configuration/settings/
# Supported icon set: https://fonts.google.com/icons

SIDEBAR_NAVIGATION = [
    {
        "title": _("Dashboard"),
        "items": [
            {
                "title": _("Dashboard"),
                "icon": "dashboard",
                "link": reverse_lazy("admin:index"),
                "permission": lambda request: request.user.is_superuser,
            },
        ],
    },
    {
        "title": _("NGO Food Requests"),
        "items": [
            {
                "title": _("NGO Food Requests"),
                "icon": "arrow_circle_right",
                "link": reverse_lazy("admin:app_food_request_foodrequest_changelist"),
                "permission": lambda request: request.user.is_staff,
            }
        ],
    },
    {
        "title": _("Items"),
        "items": [
            {
                "title": _("Item Offer"),
                "icon": "arrow_circle_right",
                "link": reverse_lazy("admin:app_item_itemoffer_changelist"),
            },
            {
                "title": _("Item Request"),
                "icon": "arrow_circle_left",
                "link": reverse_lazy("admin:app_item_itemrequest_changelist"),
            },
            {
                "title": _("Categories"),
                "icon": "inventory_2",
                "link": reverse_lazy("admin:app_item_category_changelist"),
            },
            {
                "title": _("Textile Category"),
                "icon": "package_2",
                "link": reverse_lazy("admin:app_item_textilecategory_changelist"),
            },
        ],
    },
    {
        "title": _("Transport Services"),
        "items": [
            {
                "title": _("Transport Service Offer"),
                "icon": "arrow_circle_right",
                "link": reverse_lazy("admin:app_transport_service_transportserviceoffer_changelist"),
            },
            {
                "title": _("Transport Service Request"),
                "icon": "arrow_circle_left",
                "link": reverse_lazy("admin:app_transport_service_transportservicerequest_changelist"),
            },
            {
                "title": _("Categories"),
                "icon": "inventory_2",
                "link": reverse_lazy("admin:app_transport_service_category_changelist"),
            },
        ],
    },
    {
        "title": _("Volunteering"),
        "items": [
            {
                "title": _("Volunteering Offer"),
                "icon": "arrow_circle_right",
                "link": reverse_lazy("admin:app_volunteering_volunteeringoffer_changelist"),
            },
            {
                "title": _("Volunteering Request"),
                "icon": "arrow_circle_left",
                "link": reverse_lazy("admin:app_volunteering_volunteeringrequest_changelist"),
            },
            {
                "title": _("Categories"),
                "icon": "inventory_2",
                "link": reverse_lazy("admin:app_volunteering_type_changelist"),
            },
        ],
    },
    {
        "title": _("Other"),
        "items": [
            {
                "title": _("Other Offer"),
                "icon": "arrow_circle_right",
                "link": reverse_lazy("admin:app_other_otheroffer_changelist"),
            },
            {
                "title": _("Other Request"),
                "icon": "arrow_circle_left",
                "link": reverse_lazy("admin:app_other_otherrequest_changelist"),
            },
            {
                "title": _("Categories"),
                "icon": "inventory_2",
                "link": reverse_lazy("admin:app_other_category_changelist"),
            },
        ],
    },
    {
        "title": _("Users"),
        "items": [
            {
                "title": _("Users"),
                "icon": "person",
                "link": reverse_lazy("admin:app_account_customuser_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Groups"),
                "icon": "group",
                "link": reverse_lazy("admin:auth_group_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Email Addresses"),
                "icon": "email",
                "link": reverse_lazy("admin:account_emailaddress_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Auth Tokens"),
                "icon": "vpn_key",
                "link": reverse_lazy("admin:authtoken_tokenproxy_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Impersonation Logs"),
                "icon": "supervised_user_circle",
                "link": reverse_lazy("impersonate-list"),
                "permission": lambda request: request.user.is_superuser,
            },
        ],
    },
    {
        "title": _("Background Tasks"),
        "items": [
            {
                "title": _("Failed tasks"),
                "icon": "assignment_late",
                "link": reverse_lazy("admin:django_q_failure_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Queued tasks"),
                "icon": "assignment_add",
                "link": reverse_lazy("admin:django_q_ormq_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Scheduled tasks"),
                "icon": "assignment",
                "link": reverse_lazy("admin:django_q_schedule_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Success tasks"),
                "icon": "assignment_turned_in",
                "link": reverse_lazy("admin:django_q_success_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
        ],
    },
    {
        "title": _("Social Accounts"),
        "items": [
            {
                "title": _("Social Accounts"),
                "icon": "group",
                "link": reverse_lazy("admin:socialaccount_socialaccount_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Social Apps"),
                "icon": "apps",
                "link": reverse_lazy("admin:socialaccount_socialapp_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Social Tokens"),
                "icon": "vpn_key",
                "link": reverse_lazy("admin:socialaccount_socialtoken_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
        ],
    },
]

UNFOLD = {
    "SITE_HEADER": ADMIN_TITLE,
    "SITE_TITLE": ADMIN_TITLE,
    "SITE_SYMBOL": "support",
    # https://unfoldadmin.com/docs/configuration/settings/
    # Site configuration
    # "ENVIRONMENT": "redirectioneaza.callbacks.environment_callback",
    "DASHBOARD_CALLBACK": "revm_site.callbacks.dashboard",
    # Site customization
    "SITE_ICON": lambda request: static("jazzmin/img/sprijin-de-urgenta-logo.svg"),
    "SITE_LOGO": lambda request: static("jazzmin/img/sprijin-de-urgenta-logo.svg"),
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "16x16",
            "type": "image/png",
            "href": lambda request: static("images/favicon/favicon-16x16.png"),
        },
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: static("images/favicon/favicon-32x32.png"),
        },
    ],
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            50: "#eff7ff",
            100: "#dbedfe",
            200: "#bfe0fe",
            300: "#93cefd",
            400: "#60b2fa",
            500: "#3b92f6",
            600: "#2574eb",
            700: "#1d5ed8",
            800: "#1d49a7",
            900: "#1e438a",
            950: "#172a54",
        },
    },
    # Sidebar settings
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": SIDEBAR_NAVIGATION,
    },
}
