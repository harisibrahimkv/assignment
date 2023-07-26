import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = ("app",)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "emails.db"),
    }
}
USE_TZ = True

SECRET_KEY = "4cCI6MTYzOTQ0NzgwNiwiaWF0IjoxNjM5NDQ3ODA2fQ"
