from datetime import date

import pytest

from json_store import load_json, save_json
from pr2 import service


@pytest.fixture
def state():
    return load_json("data/sample.json")


def test_submit_cancel_and_resubmit(state):
    args = (state, "Новая тема", "Аннотация", 1, 1)
    talk = service.submit_talk(*args, today=date(2026, 12, 1))
    with pytest.raises(ValueError):
        service.submit_talk(*args, today=date(2026, 12, 1))
    service.cancel_talk(state, talk["id"])
    assert service.submit_talk(*args, today=date(2026, 12, 1))["id"] != talk["id"]


def test_full_section(state):
    state["sections"][0]["capacity"] = 1
    with pytest.raises(ValueError, match="переполнена"):
        service.submit_talk(state, "Тема", "Текст", 1, 1, date(2026, 11, 1))
    assert len(state["talks"]) == 4


def test_expired_deadline(state):
    with pytest.raises(ValueError, match="завершён"):
        service.submit_talk(state, "Тема", "Текст", 1, 1, date(2026, 12, 2))


def test_search_filter_sort(state):
    assert len(service.search_talks(state, "СЕРВИС")) == 1
    assert len(list(service.filter_sections(state, 12))) == 2
    assert [item["capacity"] for item in service.sort_sections(state)] == [10, 12, 15]


def test_create_entities(state):
    conference = service.add_conference(state, "Новая", "2027-05-01", "2027-04-01", "Москва")
    student = service.add_student(state, "Иван", "А-1")
    section = service.add_section(state, "Секция", conference["id"], 1)
    talk = service.submit_talk(
        state, "Тема", "Текст", student["id"], section["id"], date(2027, 4, 1)
    )
    assert talk["student_id"] == student["id"]


def test_roundtrip(state, tmp_path):
    target = tmp_path / "state.json"
    save_json(state, target)
    assert load_json(target) == state


@pytest.mark.parametrize(
    "mutation",
    [
        lambda s: s["students"].append(s["students"][0]),
        lambda s: s["sections"][0].update(conference_id=999),
        lambda s: s["talks"][0].update(student_id=999),
        lambda s: s["talks"][0].update(is_cancelled="false"),
        lambda s: s["sections"][0].update(capacity=0),
        lambda s: s["conferences"][0].update(deadline="bad"),
        lambda s: s["students"][0].update(name=" "),
    ],
)
def test_invalid_snapshot_preserves_file(state, tmp_path, mutation):
    target = tmp_path / "state.json"
    save_json(state, target)
    original = target.read_bytes()
    mutation(state)
    with pytest.raises(ValueError):
        save_json(state, target)
    assert target.read_bytes() == original


def test_corrupt_json(tmp_path):
    target = tmp_path / "state.json"
    target.write_text("broken")
    with pytest.raises(ValueError):
        load_json(target)
    assert target.read_text() == "broken"
