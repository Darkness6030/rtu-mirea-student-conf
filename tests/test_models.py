from datetime import date

import pytest

import services
from storage import load_state, save_state


@pytest.fixture
def state():
    return load_state("data/sample.json")


def test_shared_object_identity_after_roundtrip(state, tmp_path):
    target = tmp_path / "snapshot.json"
    services.cancel_talk(state, 1)
    save_state(state, target)
    restored = load_state(target)
    talk = restored["talks"][0]
    assert talk.student is restored["students"][0]
    assert talk.section is restored["sections"][0]
    assert talk.section.conference is restored["conferences"][0]
    assert talk.status == "Отменён"
    with pytest.raises(AttributeError):
        talk.is_cancelled = False


def test_submit_cancel_and_resubmit(state):
    services.add_conference(state, "Новая", "2027-05-01", "2027-04-01", "Москва")
    services.add_student(state, "Иван", "А-1")
    services.add_section(state, "Новая секция", 3, 1)
    args = (state, "Тема", "Текст", 4, 4, date(2027, 4, 1))
    talk = services.submit_talk(*args)
    with pytest.raises(ValueError):
        services.submit_talk(*args)
    services.cancel_talk(state, talk.id)
    replacement = services.submit_talk(*args)
    assert talk.is_cancelled
    assert not replacement.is_cancelled
    assert replacement.id != talk.id
    with pytest.raises(ValueError):
        services.submit_talk(state, "Другая", "Текст", 4, 4, date(2027, 4, 1))


@pytest.mark.parametrize(
    "student,section,day",
    [
        (999, 1, date(2026, 11, 1)),
        (1, 999, date(2026, 11, 1)),
        (1, 1, date(2026, 12, 2)),
    ],
)
def test_invalid_submission_is_atomic(state, student, section, day):
    with pytest.raises(ValueError):
        services.submit_talk(state, "Тема", "Текст", student, section, day)
    assert len(state["talks"]) == 4


def test_search_filter_sort(state):
    assert len(services.search_talks(state, "СЕРВИС")) == 1
    assert len(list(services.filter_sections(state, 12))) == 2
    assert [item.capacity for item in services.sort_sections(state)] == [10, 12, 15]


def test_empty_title(state):
    with pytest.raises(ValueError):
        services.submit_talk(state, " ", "Текст", 1, 1, date(2026, 11, 1))
