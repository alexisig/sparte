"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
hello world
"""
from pathlib import Path

import environ
import pkg_resources
import sentry_sdk
from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

OFFICIAL_VERSION = "2.4.0"

root = environ.Path(__file__) - 2  # get root of the project
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(root())

# initialize env with environment variable
# it can contains DEBUG (in production env it shall)
# so we could explore how to load file only on local execution
env = environ.Env()

env_path = BASE_DIR / ".env"
if env_path.is_file():
    environ.Env.read_env(str(env_path))  # reading .env file

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Should be one of : local, staging, production
ENVIRONMENT = env.str("ENVIRONMENT")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)
USE_SRI = env.bool("USE_SRI", default=False) or not DEBUG

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

DOMAIN_URL = env.str("DOMAIN_URL")

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.contrib.humanize",
]

RESTFRAMEWORK_APPS = [
    "rest_framework",
    "rest_framework_gis",
]

THIRD_APPS = [
    "import_export",
    "crispy_forms",
    "django_app_parameter",
    "sri",
    # "widget_tweaks",
    "django_celery_results",
    # "django_docx_template",
]

# upper app should not communicate with lower ones
PROJECT_APPS = [
    "django_docx_template",
    "utils.apps.UtilsConfig",
    "users.apps.UsersConfig",
    "carto.apps.CartoConfig",
    "public_data.apps.PublicDataConfig",
    "project.apps.ProjectConfig",
    "home.apps.HomeConfig",
    "highcharts.apps.HighchartsConfig",
]

INSTALLED_APPS = DJANGO_APPS + RESTFRAMEWORK_APPS + THIRD_APPS + PROJECT_APPS


MIDDLEWARE = [
    "config.middlewares.LogIncomingRequest",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

USE_CSP = env.bool("USE_CSP", default=False) or not DEBUG
if USE_CSP:
    MIDDLEWARE.insert(2, "csp.middleware.CSPMiddleware")


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "users.context_processors.add_connected_user_to_context",
                "django_app_parameter.context_processors.add_global_parameter_context",
                "csp.context_processors.nonce",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# require DATABASE_URL in .env file
DATABASES = {
    "default": env.db(),
}
# force postgis to avoid any surprise
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# indicate the new User model to Django
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "project:list"
LOGIN_URL = "users:signin"


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Bucket S3 and filestorage
# see https://django-storages.readthedocs.io/en/latest/
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# credentials
AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", default="")

# bucket name and region
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME", default="")
AWS_S3_REGION_NAME = env.str("AWS_S3_REGION_NAME", default="eu-west-3")

# append a prefix to all uploaded file (useful to not mix local, staging...)
AWS_LOCATION = env.str("AWS_LOCATION", default="local")
# avoid overriding a file if same key is provided
AWS_S3_FILE_OVERWRITE = False
# allow signed url to be accessed from all regions
AWS_S3_SIGNATURE_VERSION = "s3v4"

# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

STATICFILES_DIRS = [
    BASE_DIR / "static",
    # BASE_DIR / "htmlcov",
]

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticroot")


PUBLIC_MEDIA_LOCATION = "media"
MEDIA_URL = (
    f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{PUBLIC_MEDIA_LOCATION}/"
)


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Django.contrib.messages
# tag for bootstrap compatibility

MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "primary",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}
# default is INFO
if DEBUG is True:
    MESSAGE_LEVEL = messages.DEBUG


# django-import-export
# https://django-import-export.readthedocs.io/en/latest/
IMPORT_EXPORT_USE_TRANSACTIONS = True


# Crispy configuration
# https://django-crispy-forms.readthedocs.io/en/latest/index.html
# set default rendering
# CRISPY_TEMPLATE_PACK = "bootstrap4"
CRISPY_CLASS_CONVERTERS = {
    "textinput": "fr-input",
    "urlinput": "fr-input",
    "numberinput": "fr-input",
    "emailinput": "fr-input",
    "dateinput": "fr-input",
    "textarea": "fr-input",
    "passwordinput": "fr-input",
    "select": "fr-select",
    "label": "fr-label"
}

# Celery configuration
default_redis = "redis://redis:6379/0"
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default=default_redis)
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", default=default_redis)
CELERY_ACKS_LATE = True
CELERY_RESULT_EXTENDED = True

# django-debug-toolbar configuration

# activate only if debug is True
# and only if package is available
if DEBUG:
    try:
        # only if debug_toolbar is available, else it will fire exception
        # useful to turn debug mode on staging without installing dev dependencies
        import debug_toolbar  # noqa: F401

        INSTALLED_APPS += ["debug_toolbar"]
        MIDDLEWARE += [
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ]

        # bypass check of internal IPs
        def show_toolbar(request):
            return True

        DEBUG_TOOLBAR_CONFIG = {
            "SHOW_TOOLBAR_CALLBACK": show_toolbar,
        }

    except ImportError:
        pass


DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "djt_csp.panel.SecurityPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
]


# DJANGO DOCX TEMPLATES
DJANGO_DOCX_TEMPLATES = {
    "data_sources": [
        "project.datasources.DiagnosticSource",
    ],
    "base_template": "index.html",
}

# Configuration for highchart
HIGHCHART_SERVER = env.str("HIGHCHART_SERVER", default="https://export.highcharts.com/")

# EMAIL
"""Configuration of e-mails

Several configuration are authorized, see available_engines variable below.

Local = will store email to a file (not sending)
mailjet = will use mailjet provider to send emails, it uses anymail lib, see
https://anymail.readthedocs.io/en/stable/esps/mailjet/

To set local configuration, please add to .env file following variables:
- EMAIL_ENGINE=local
- EMAIL_FILE_PATH where to store a file for each sent email

To set MailJet configuration, please add environment variables:
- EMAIL_ENGINE=mailjet
- MAILJET_ID & MAILJET_SECRET, see https://app.mailjet.com/account/api_keys
"""

EMAIL_ENGINE = env.str("EMAIL_ENGINE", default="local")

available_engines = ["local", "mailjet"]
if EMAIL_ENGINE not in available_engines:
    raise ImproperlyConfigured("E-mail backend needs to be correctly set")


if EMAIL_ENGINE == "local":
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    emails_dirpath = BASE_DIR / "emails"
    EMAIL_FILE_PATH = env.str("EMAIL_FILE_PATH", default=emails_dirpath)

elif EMAIL_ENGINE == "mailjet":
    INSTALLED_APPS += [
        "anymail",
    ]
    EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
    ANYMAIL = {
        "MAILJET_API_KEY": env.str("MAILJET_ID"),
        "MAILJET_SECRET_KEY": env.str("MAILJET_SECRET"),
    }

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="johndoe@email.com")

# Jupyter configuration

# used by ./manage.py shell_plus --notebook
if "django-extensions" in {pkg.key for pkg in pkg_resources.working_set}:
    INSTALLED_APPS += [
        "django_extensions",
    ]
    NOTEBOOK_ARGUMENTS = [
        "--ip",
        "0.0.0.0",
        "--allow-root",
        "--notebook-dir='notebooks/'",
        "--NotebookApp.token=''",
        "--NotebookApp.password=''",
    ]

# RESTRAMEWORK parameters
# https://www.django-rest-framework.org

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination"
}

# FORMAT SETTINGS

USE_L10N = True
LANGUAGE_CODE = "fr"
USE_THOUSAND_SEPARATOR = True
DECIMAL_SEPARATOR = ","
THOUSAND_SEPARATOR = " "
NUMBER_GROUPING = 3


# SENTRY
if ENVIRONMENT != "local":
    sentry_sdk.init(
        # dsn="https://a227bee32f4f41c2a60e9292ce4d033e@o548798.ingest.sentry.io/6068271",
        dsn="https://b40bb226b8a148fdafff102baf5abf34@sentry.incubateur.net/21",
        integrations=[
            DjangoIntegration(
                # available options:
                # url (default) - formats based on the route
                # function_name - formats based on the view function name
                transaction_style="url",
            ),
            RedisIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
        # By default the SDK will try to use the SENTRY_RELEASE
        # environment variable, or infer a git commit
        # SHA as release, however you may want to set
        # something more human-readable.
        release=f"Sparte@{OFFICIAL_VERSION}",
        environment=ENVIRONMENT,
        debug=False,
        request_bodies="always",
        with_locals=True,
    )


# MATOMO

MATOMO_TOKEN = env.str("MATOMO_TOKEN", default="")
MATOMO_ACTIVATE = env.bool("MATOMO_ACTIVATE", default=False)

# SECURITY - Content Security Header Policy
# https://django-csp.readthedocs.io

CSP_UPGRADE_INSECURE_REQUESTS = not DEBUG
CSP_DEFAULT_SRC = ["'self'"]
CSP_SCRIPT_SRC = [
    "'self'",
    "https://stats.data.gouv.fr",
    "https://code.highcharts.com",
    STATIC_URL,
]
CSP_STYLE_SRC = [
    "'self'",
    # "'unsafe-inline'",
    "https://cdn.jsdelivr.net",
    STATIC_URL,
]
CSP_IMG_SRC = ["'self'", "https://wxs.ign.fr", "data:", MEDIA_URL, STATIC_URL]
CSP_INCLUDE_NONCE_IN = ["script-src", "style-src"]
CSP_FONT_SRC = ("'self'", "data:", "https://cdn.jsdelivr.net", STATIC_URL)
CSP_CONNECT_SRC = ["https://stats.data.gouv.fr", "'self'"]


# MAP SETTINGS

ORTHOPHOTO_URL = (
    "https://wxs.ign.fr/ortho/geoportail/wmts?"
    "&REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&TILEMATRIXSET=PM"
    "&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&STYLE=normal&FORMAT=image/jpeg"
    "&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}"
)

# MATTERMOST SETTINGS

# the webhook needs to be generated in mattermost and is linked to a active account
MATTERMOST_URL = env.str("MATTERMOST_WEBHOOK", default=None)

# ALERT DIAGNOSTICS BLOCKED

ALERT_DIAG_MEDIUM = env.str("ALERT_DIAG_MEDIUM", default="both")
if ALERT_DIAG_MEDIUM not in ["mattermost", "email", "both"]:
    raise ImproperlyConfigured("ALERT_DIAG_MEDIUM needs to be correctly set")
ALERT_DIAG_EMAIL_RECIPIENTS = env.list("ALERT_DIAG_EMAIL_RECIPIENTS", default=[])
ALERT_DIAG_MATTERMOST_RECIPIENTS = env.list(
    "ALERT_DIAG_MATTERMOST_RECIPIENTS", default=[]
)

# LOGGING SETTINGS

LOGGING_LEVEL = env.str("LOGGING_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "just_message": {
            "format": "[{asctime}] {message}",
            "style": "{",
            "datefmt": "%d%m%Y %H%M%S",
        },
        "verbose": {
            "format": "[{asctime}]{levelname:<7} {module} {process:d} {thread:d} {message}",
            "style": "{",
            "datefmt": "%d%m%Y %H%M%S",
        },
        "simple": {
            "format": "[{asctime}]{levelname:<7} {message}",
            "style": "{",
            "datefmt": "%d%m%Y %H%M%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "console_just_message": {
            "class": "logging.StreamHandler",
            "formatter": "just_message",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "config": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "public_data": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "management.commands": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
    },
}
