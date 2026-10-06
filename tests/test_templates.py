from pathlib import Path
from types import SimpleNamespace

import pytest
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.test import override_settings

from models import Talk
from storage import load_json, save_json

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize(
    "path,template",
    [
        ("/", "homepage/index.html"),
        ("/conferences/", "conferences/conference_list.html"),
        ("/conferences/1/", "conferences/conference_detail.html"),
        ("/students/", "students/student_list.html"),
        ("/students/1/", "students/student_detail.html"),
        ("/sections/", "sections/section_list.html"),
        ("/sections/1/", "sections/section_detail.html"),
        ("/talks/", "talks/talk_list.html"),
        ("/talks/1/", "talks/talk_detail.html"),
        ("/missing/", "404.html"),
    ],
)
def test_inheritance_and_navigation(client, path, template):
    response = client.get(path)
    used = {item.name for item in response.templates}
    assert {template, "base.html", "includes/navigation.html"} <= used
    assert response.content.decode().count('<html lang="ru">') == 1


def test_context_contains_domain_objects(client):
    response = client.get("/talks/1/")
    talk = response.context["talk"]
    assert isinstance(talk, Talk)
    assert talk.student.name in response.content.decode()
    assert talk.section.conference.name in response.content.decode()


def test_reused_card_and_status_templates(client):
    for path in ("/talks/", "/students/1/", "/sections/1/"):
        used = {item.name for item in client.get(path).templates}
        assert "talks/includes/talk_card.html" in used
        assert "talks/includes/talk_status.html" in used


def test_static_tag_uses_configured_prefix(client):
    assets = (
        "vendor/bootstrap.min.css",
        "homepage/css/style.css",
        "homepage/img/logo.svg",
        "homepage/js/main.js",
    )
    with override_settings(STATIC_URL="/assets/"):
        html = client.get("/").content.decode()
        for asset in assets:
            assert f"/assets/{asset}" in html
            assert finders.find(asset)


def test_filters_keep_full_abstract_on_detail(client, tmp_path):
    data = load_json(ROOT / "data/sample.json")
    data["talks"][0]["abstract"] = " ".join(f"слово{i}" for i in range(1, 31))
    save_json(data, tmp_path / "runtime.json")
    listing = client.get("/talks/").content.decode()
    assert "Всего: 4" in listing
    assert "слово20" in listing and "слово30" not in listing
    assert "слово30" in client.get("/talks/1/").content.decode()
    assert "18.12.2026" in client.get("/conferences/1/").content.decode()


def test_default_title_in_card():
    conference = SimpleNamespace(id=1, name="", location="Москва", is_open=True)
    html = render_to_string(
        "conferences/includes/conference_card.html",
        {
            "conference": conference,
        },
    )
    assert "Без названия" in html


@pytest.mark.parametrize("path", ["/students/1/", "/sections/1/", "/conferences/1/"])
def test_empty_related_collections(client, tmp_path, path):
    data = load_json(ROOT / "data/sample.json")
    data["talks"] = []
    if path.startswith("/conferences/"):
        data["sections"] = []
    save_json(data, tmp_path / "runtime.json")
    response = client.get(path)
    assert response.status_code == 200
    assert "Записей пока нет" in response.content.decode()
