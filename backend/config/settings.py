import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(
    BASE_DIR / ".env",
)


def get_bool_env(name, default=False):
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def get_list_env(name, default=""):
    value = os.getenv(
        name,
        default,
    )

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
)

if not SECRET_KEY:
    raise RuntimeError(
        "DJANGO_SECRET_KEY не задан в .env",
    )


DEBUG = get_bool_env(
    "DJANGO_DEBUG",
    True,
)


ALLOWED_HOSTS = get_list_env(
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1,localhost",
)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "accounts",
    "storage",
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": (
            "django.template.backends."
            "django.DjangoTemplates"
        ),
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                (
                    "django.template.context_processors."
                    "debug"
                ),
                (
                    "django.template.context_processors."
                    "request"
                ),
                (
                    "django.contrib.auth.context_processors."
                    "auth"
                ),
                (
                    "django.contrib.messages.context_processors."
                    "messages"
                ),
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv(
            "POSTGRES_DB",
            "my_cloud",
        ),
        "USER": os.getenv(
            "POSTGRES_USER",
            "my_cloud_user",
        ),
        "PASSWORD": os.getenv(
            "POSTGRES_PASSWORD",
            "my_cloud_password",
        ),
        "HOST": os.getenv(
            "POSTGRES_HOST",
            "127.0.0.1",
        ),
        "PORT": os.getenv(
            "POSTGRES_PORT",
            "5432",
        ),
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


LANGUAGE_CODE = "ru-ru"


TIME_ZONE = "Europe/Moscow"


USE_I18N = True


USE_TZ = True


STATIC_URL = "static/"


STATIC_ROOT = BASE_DIR / "staticfiles"


STATICFILES_DIRS = [
    BASE_DIR / "static",
]


MEDIA_URL = "media/"


MEDIA_ROOT = BASE_DIR / "media"


MAX_UPLOAD_SIZE_MB = int(
    os.getenv(
        "MAX_UPLOAD_SIZE_MB",
        "100",
    ),
)


MAX_UPLOAD_SIZE_BYTES = (
    MAX_UPLOAD_SIZE_MB
    * 1024
    * 1024
)


DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)


AUTH_USER_MODEL = "accounts.User"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        (
            "rest_framework.authentication."
            "SessionAuthentication"
        ),
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        (
            "rest_framework.permissions."
            "IsAuthenticated"
        ),
    ],
}


CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


CSRF_COOKIE_HTTPONLY = False


CSRF_COOKIE_SAMESITE = "Lax"


SESSION_COOKIE_SAMESITE = "Lax"


SESSION_COOKIE_HTTPONLY = True


SECURE_SSL_REDIRECT = get_bool_env(
    "DJANGO_SECURE_SSL_REDIRECT",
    False,
)


SESSION_COOKIE_SECURE = get_bool_env(
    "DJANGO_SESSION_COOKIE_SECURE",
    False,
)


CSRF_COOKIE_SECURE = get_bool_env(
    "DJANGO_CSRF_COOKIE_SECURE",
    False,
)


SECURE_HSTS_SECONDS = int(
    os.getenv(
        "DJANGO_SECURE_HSTS_SECONDS",
        "0",
    ),
)


SECURE_HSTS_INCLUDE_SUBDOMAINS = get_bool_env(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    False,
)


SECURE_HSTS_PRELOAD = get_bool_env(
    "DJANGO_SECURE_HSTS_PRELOAD",
    False,
)


PUBLIC_FILE_BASE_URL = os.getenv(
    "PUBLIC_FILE_BASE_URL",
    "http://127.0.0.1:8000/api/files/public",
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "{asctime} [{levelname}] "
                "{name}: {message}"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": [
                "console",
            ],
            "level": "INFO",
            "propagate": False,
        },
        "accounts": {
            "handlers": [
                "console",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
        "storage": {
            "handlers": [
                "console",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}