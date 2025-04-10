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
    "jazzmin",
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


# django-jazzmin
# -------------------------------------------------------------------------------
# django-jazzmin - https://django-jazzmin.readthedocs.io/configuration/

JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": ADMIN_TITLE,
    # Title on the brand, and the login screen (19 chars max)
    "site_header": ADMIN_TITLE,
    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    "site_logo": "jazzmin/img/sprijin-de-urgenta.svg",
    "site_logo_short": "jazzmin/img/sprijin-de-urgenta-logo.svg",
    "site_icon": "jazzmin/img/sprijin-de-urgenta-logo.svg",
    "site_logo_classes": "site-logo",
    # Welcome text on the login screen
    "welcome_sign": "",
    # Copyright on the footer
    "copyright": "Code4Romania - War Task Force",
    # The model admin to search from the search bar, search bar omitted if excluded
    # "search_model": "donors.Donor",
    # The field name on user model that contains avatar image
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        # external url that opens in a new window (Permissions can be added)
        # {
        #     "name": "View website",
        #     "url": "https://github.com/farridav/django-jazzmin/issues",
        #     "new_window": True,
        # },
        # model admin to link to (Permissions checked against model)
        # {"model": "auth.User"},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        # {
        #     "name": "Support",
        #     "url": "https://github.com/farridav/django-jazzmin/issues",
        #     "new_window": True,
        # },
        {"model": "auth.user", "new_window": False},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to auto expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        "app_food_request",
        "app_item",
        "app_item.itemoffer",
        "app_item.itemrequest",
        "app_item.category",
        "app_item.textilecategory",
        "app_transport_service",
        "app_transport_service.transportserviceoffer",
        "app_transport_service.transportservicerequest",
        "app_transport_service.category",
        "app_volunteering",
        "app_volunteering.volunteeringoffer",
        "app_volunteering.volunteeringrequest",
        "app_volunteering.category",
        "app_other",
        "app_other.otheroffer",
        "app_other.otherrequest",
        "app_other.category",
        "auth",
        "app_account",
        "django_q",
        "django_q.schedule",
        "django_q.success",
        "django_q.failed",
        "account",
        "socialaccount",
        "socialaccount.socialaccount",
        "socialaccount.socialapp",
        "socialaccount.socialtoken",
        "authtoken",
        "authtoken.tokenproxy",
    ],
    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [
            {
                "name": "Make Messages",
                "url": "make_messages",
                "icon": "fas fa-comments",
                "permissions": ["books.view_book"],
            }
        ]
    },
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free
    # for a list of icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "account": "fas fa-envelope",
        "account.EmailAddress": "fas fa-at",
        "app_account": "fas fa-users",
        "app_account.CustomUser": "fas fa-user",
        "django_q": "fas fa-layer-group",
        "django_q.schedule": "fas fa-layer-group",
        "django_q.success": "fas fa-check",
        "django_q.failure": "fas fa-exclamation",
        "socialaccount": "fas fa-share-nodes",
        "socialaccount.socialaccount": "fas fa-hashtag",
        "socialaccount.socialapp": "fas fa-user-cog",
        "socialaccount.socialtoken": "fas fa-user-lock",
        "authtoken": "fas fa-lock",
        "authtoken.tokenproxy": "fas fa-user-lock",
        "app_food_request.FoodRequest": "far fa-arrow-alt-circle-left",
        "app_item.Category": "fas fa-cube",
        "app_item.TextileCategory": "fas fa-cubes",
        "app_item.ItemOffer": "fas fa-arrow-alt-circle-right",
        "app_item.ItemRequest": "far fa-arrow-alt-circle-left",
        "app_other.Category": "fas fa-cube",
        "app_other.Subcategory": "fas fa-cubes",
        "app_other.OtherOffer": "fas fa-arrow-alt-circle-right",
        "app_other.OtherRequest": "far fa-arrow-alt-circle-left",
        "app_volunteering.Type": "fas fa-cube",
        "app_volunteering.VolunteeringOffer": "fas fa-arrow-alt-circle-right",
        "app_volunteering.VolunteeringRequest": "far fa-arrow-alt-circle-left",
        "app_transport_service.Category": "fas fa-cube",
        "app_transport_service.TransportServiceOffer": "fas fa-arrow-alt-circle-right",
        "app_transport_service.TransportServiceRequest": "far fa-arrow-alt-circle-left",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "jazzmin/css/admin.css",
    "custom_js": "",
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": bool(ENVIRONMENT == "development"),
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "single",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    # Add a language dropdown into the admin
    "language_chooser": True,
}

if ENVIRONMENT == "development":
    JAZZMIN_SETTINGS["usermenu_links"].append(
        {
            "name": "Support",
            "url": "https://django-jazzmin.readthedocs.io/configuration/",
            "new_window": True,
            "icon": "fas fa-book",
        }
    )

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": "darkly",
}
