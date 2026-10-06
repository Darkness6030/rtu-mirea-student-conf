from datetime import date, timedelta

import pytest

from pr1.main import has_free_slot, is_submission_open, submission_status


@pytest.mark.parametrize(
    "count,expected", [(-1, False), (0, True), (9, True), (10, False), (11, False)]
)
def test_capacity_boundary(count, expected):
    assert has_free_slot(10, count) is expected


def test_deadline_inclusive():
    day = date(2026, 10, 6)
    assert is_submission_open(day, day)
    assert not is_submission_open(day - timedelta(days=1), day)


def test_status():
    assert submission_status(True, True) == "Доклад можно подать"
    assert submission_status(False, True) == "Подача недоступна"
