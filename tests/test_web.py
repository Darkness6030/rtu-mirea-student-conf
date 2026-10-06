"""HTTP-регрессии без базы данных: реальные маршруты и JSON ПР3."""

import os
from pathlib import Path
from html.parser import HTMLParser

import django
import pytest
from django.test import Client, override_settings
from django.urls import resolve, reverse

from json_store import load_json, save_json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studentconf.settings")
django.setup()
ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def client(tmp_path):
    with override_settings(
        DEBUG=False,
        ALLOWED_HOSTS=["testserver"],
        DATA_FILE=tmp_path / "runtime.json",
        SAMPLE_FILE=ROOT / "data/sample.json",
    ):
        yield Client()


@pytest.mark.parametrize(
    "path,expected",
    [
        ("/", "Большие идеи"),
        ("/conferences/", "Конференции"),
        ("/conferences/1/", "Студенческая наука 2026"),
        ("/students/", "Студенты"),
        ("/students/1/", "Кирьянов"),
        ("/sections/", "Секции"),
        ("/sections/1/", "Веб-разработка"),
        ("/talks/", "Доклады"),
        ("/talks/1/", "Сервис организации студенческих конференций"),
        ("/talks/4/", "Отменён"),
    ],
)
def test_pages(client, path, expected):
    response = client.get(path)
    assert response.status_code == 200
    assert expected in response.content.decode()
    assert response["Content-Type"] == "text/html; charset=utf-8"
    assert '<html lang="ru">' in response.content.decode()


@pytest.mark.parametrize(
    "path",
    [
        "/nonexistent/",
        "/conferences/999/",
        "/students/999/",
        "/sections/999/",
        "/talks/999/",
        "/talks/abc/",
        "/talks/-1/",
        "/talks/0/",
    ],
)
def test_custom_404(client, path):
    response = client.get(path)
    assert response.status_code == 404
    assert "Страница не найдена" in response.content.decode()
    assert "На главную" in response.content.decode()


@pytest.mark.parametrize(
    "namespace,parameter",
    [
        ("conferences", "conference_id"),
        ("students", "student_id"),
        ("sections", "section_id"),
        ("talks", "talk_id"),
    ],
)
def test_named_routes(namespace, parameter):
    url = reverse(f"{namespace}:detail", args=[1])
    assert resolve(url).kwargs == {parameter: 1}


def test_post_is_not_supported(client):
    assert client.post("/talks/1/").status_code == 405


def test_head(client):
    response = client.head("/talks/1/")
    assert response.status_code == 200
    assert response.content == b""


def test_html_escaping(client, tmp_path):
    raw = load_json(ROOT / "data/sample.json")
    raw["talks"][0]["title"] = '<script>alert("x")</script>'
    raw["talks"][0]["abstract"] = "<img src=x onerror=alert(1)>"
    save_json(raw, tmp_path / "runtime.json")
    for path in ("/talks/", "/talks/1/", "/students/1/", "/sections/1/"):
        html = client.get(path).content.decode()
        assert "<script>" not in html
        assert "&lt;script&gt;" in html
        assert "<img src=x" not in html


def test_read_new_snapshot_on_next_request(client, tmp_path):
    raw = load_json(ROOT / "data/sample.json")
    raw["talks"][0]["title"] = "Изменённая тема"
    save_json(raw, tmp_path / "runtime.json")
    assert "Изменённая тема" in client.get("/talks/1/").content.decode()
    raw["talks"][0]["is_cancelled"] = True
    save_json(raw, tmp_path / "runtime.json")
    assert "Отменён" in client.get("/talks/1/").content.decode()


def test_corrupt_data_not_silently_replaced(client, tmp_path):
    target = tmp_path / "runtime.json"
    target.write_text("broken")
    response = client.get("/conferences/")
    assert response.status_code == 503
    assert "Данные временно недоступны" in response.content.decode()
    assert "Traceback" not in response.content.decode()
    assert target.read_text() == "broken"


def test_empty_collections(client, tmp_path):
    save_json(
        {key: [] for key in ("conferences", "students", "sections", "talks")},
        tmp_path / "runtime.json",
    )
    for path in ("/conferences/", "/students/", "/sections/", "/talks/"):
        response = client.get(path)
        assert response.status_code == 200
        assert "Записей пока нет" in response.content.decode()


def test_all_internal_links(client):
    class Links(HTMLParser):
        def __init__(self):
            super().__init__()
            self.urls = set()

        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get("href", "")
            if tag == "a" and href.startswith("/"):
                self.urls.add(href)

    pending, seen = {"/"}, set()
    while pending:
        url = pending.pop()
        response = client.get(url)
        assert response.status_code == 200, url
        parser = Links()
        parser.feed(response.content.decode())
        seen.add(url)
        pending.update(parser.urls - seen)
    assert len(seen) == 17  # главная, 4 списка, 12 объектов


def test_section_availability(client, tmp_path):
    from unittest.mock import patch

    raw = load_json(ROOT / "data/sample.json")
    raw["sections"][0]["capacity"] = 1
    save_json(raw, tmp_path / "runtime.json")
    with patch("models.conference.Conference.is_open", return_value=True):
        assert "Мест нет" in client.get("/sections/1/").content.decode()
        raw["talks"][0]["is_cancelled"] = True
        save_json(raw, tmp_path / "runtime.json")
        assert "Есть места" in client.get("/sections/1/").content.decode()
    with patch("models.conference.Conference.is_open", return_value=False):
        assert "Приём завершён" in client.get("/sections/1/").content.decode()
