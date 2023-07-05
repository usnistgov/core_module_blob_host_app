""" Test settings
"""

SECRET_KEY = "fake-key"

SERVER_URI = "http://mock_cdcs_server"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # Extra apps
    "defender",
    "menu",
    # Local apps
    "core_main_app",
    "core_parser_app",
    "core_linked_records_app",
    "core_module_blob_host_app",
    "tests",
]

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core_main_app.utils.custom_context_processors.domain_context_processor",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

# TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

MONGODB_INDEXING = False
MONGODB_ASYNC_SAVE = False

ENABLE_SAML2_SSO_AUTH = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

ID_PROVIDER_SYSTEM_NAME = "mock_provider_system"
