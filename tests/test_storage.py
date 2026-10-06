import pytest

from storage import load_json, save_json


@pytest.fixture
def state():
    return load_json("data/sample.json")


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
