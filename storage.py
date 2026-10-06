"""Атомарное сохранение проверенного снимка JSON."""

import json
import os
import tempfile
from pathlib import Path

from validation import validate_state
from models import Conference, Section, Student, Talk


def load_json(path: str | Path) -> dict:
    with Path(path).open(encoding="utf-8") as stream:
        state = json.load(stream)
    validate_state(state)
    return state


def save_json(state: dict, path: str | Path) -> None:
    validate_state(state)
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = Path(stream.name)
            json.dump(state, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def load_state(path: str | Path) -> dict:
    raw = load_json(path)
    conferences = {item["id"]: Conference.from_dict(item) for item in raw["conferences"]}
    students = {item["id"]: Student.from_dict(item) for item in raw["students"]}
    sections = {
        item["id"]: Section(
            item["id"], item["name"], conferences[item["conference_id"]], item["capacity"]
        )
        for item in raw["sections"]
    }
    talks = [
        Talk(
            item["id"],
            item["title"],
            item["abstract"],
            students[item["student_id"]],
            sections[item["section_id"]],
            item["is_cancelled"],
        )
        for item in raw["talks"]
    ]
    return {
        "conferences": list(conferences.values()),
        "students": list(students.values()),
        "sections": list(sections.values()),
        "talks": talks,
    }


def save_state(state: dict, path: str | Path) -> None:
    save_json({name: [item.to_dict() for item in items] for name, items in state.items()}, path)
