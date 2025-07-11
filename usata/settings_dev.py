from .settings import *  # noqa


SECRET_KEY = "django-insecure-c-#d#c9q(n8*26b!d^tjml(-kvosxg-!%hl5!%3urejan&on-b"

ALLOWED_HOSTS.append("*")  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa
    }
}

DEBUG = True
