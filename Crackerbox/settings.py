import json
import os
import sqlite3
from os.path import expanduser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEBUG = False

home_directory = expanduser("~")

with open(home_directory + "/.env") as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        return os.environ[setting]


SECRET_KEY = get_secret("SECRET_KEY")

if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {"level": "INFO", "handlers": ["file"]},
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": "/home/quizzer/logs/django.log",
                "formatter": "app",
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
                "include_html": True,
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "level": "INFO",
                "propagate": True,
            },
        },
        "formatters": {
            "app": {
                "format": (
                    "%(asctime)s [%(levelname)-8s] "
                    "(%(module)s.%(funcName)s) %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
    }

    ALLOWED_HOSTS = [
        "165.232.40.239",
        "studyquizzer.com",
        "www.studyquizzer.com",
    ]

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "HOST": "localhost",
            "port": "",
            "NAME": "studyquizzer",
            "USER": "quizzeruser",
            "PASSWORD": get_secret("DB_PASSWORD"),
        }
    }

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

AUTH_USER_MODEL = "users.User"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest",
    "django.forms",
    "rest_framework",
    "annoying",
    "crispy_forms",
    "crackerbox_",
    "django_cleanup",
    "users.apps.UsersConfig",
    "qa.apps.QaConfig",
    "user_profile",
    "MultiChoice",
    "material",
    "taggit",
    "hitcount",
    "sorl.thumbnail",
    "chat",
    "django_archive",
    "widget_tweaks",
    "martor",
    "notifications",
    "django_q",
]

QA_SETTINGS = {
    "qa_messages": True,
    "qa_description_optional": False,
    "reputation": {
        "CREATE_QUESTION": 0,
        "CREATE_ANSWER": 0,
        "CREATE_ANSWER_COMMENT": 0,
        "CREATE_QUESTION_COMMENT": 0,
        "ACCEPT_ANSWER": 0,
        "UPVOTE_QUESTION": 0,
        "UPVOTE_ANSWER": 0,
        "DOWNVOTE_QUESTION": 0,
        "DOWNVOTE_ANSWER": 0,
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

X_FRAME_OPTIONS = "SAMEORIGIN"

ROOT_URLCONF = "Crackerbox.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = "bootstrap4"
CRACKERBOX_MAX_UPLOAD = 42 * 1024 * 1024

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_L10N = True

USE_TZ = True

MARKDOWN_EDITOR_SKIN = "simple"


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

CSRF_COOKIE_SECURE = True

LOGIN_REDIRECT_URL = "home"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "ds2-eude-ss.host.gl"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "noreply@studyquizzer.com"
EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")

DATA_UPLOAD_MAX_MEMORY_SIZE = None

Q_CLUSTER = {
    "name": "study_quizzer_daemon",
    "workers": 8,
    "recycle": 500,
    "timeout": 60,
    "compress": True,
    "save_limit": 250,
    "queue_limit": 500,
    "cpu_affinity": 2,
    "max_attempts": 0,
    "label": "Django Q",
    "redis": {
        "host": "localhost",
        "port": 6379,
        "password": get_secret("REDIS_PASSWORD"),
        "db": 0,
    },
    "error_reporter": {
        "sentry": {
            "dsn": "https://e11b005dc7a64be6b986c2eee149d08c@o470042.ingest.sentry.io/5500226",
        }
    },
}

ADMINS = [
    ("Shepherd", "shepherd@studyquizzer.com"),
]
MANAGERS = [
    ("Shepherd", "shepherd@studyquizzer.com"),
]

DJANGO_NOTIFICATIONS_CONFIG = {"SOFT_DELETE": True}

connection = sqlite3.connect(f"{BASE_DIR}/Crackerbox/mcq_distractors.db")
cursor = connection.cursor()
