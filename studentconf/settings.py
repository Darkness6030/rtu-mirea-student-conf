"""Настройки учебного веб-слоя ПР5 без базы данных и ORM."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "local-pr5-demo-not-for-deployment")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "[::1]"]
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "homepage",
    "conferences",
    "students",
    "sections",
    "talks",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "studentconf.urls"
TEMPLATES = []
WSGI_APPLICATION = "studentconf.wsgi.application"
DATABASES = {}
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_TZ = True
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
# Один снимок на запрос. Изменения из консоли видны после обновления страницы.
DATA_FILE = Path(os.environ.get("CONFERENCE_DATA_FILE", BASE_DIR / "data" / "runtime.json"))
SAMPLE_FILE = BASE_DIR / "data" / "sample.json"
