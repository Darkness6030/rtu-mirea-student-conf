import os
from pathlib import Path

import django
import pytest
from django.test import Client, override_settings
from django.test.utils import setup_test_environment, teardown_test_environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studentconf.settings")
django.setup()
ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session", autouse=True)
def template_test_environment():
    setup_test_environment()
    yield
    teardown_test_environment()


@pytest.fixture
def client(tmp_path):
    with override_settings(
        DEBUG=False,
        ALLOWED_HOSTS=["testserver"],
        DATA_FILE=tmp_path / "runtime.json",
        SAMPLE_FILE=ROOT / "data/sample.json",
    ):
        yield Client()
