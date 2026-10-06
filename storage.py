"""ПР3: сериализация и восстановление графа объектов из совместимого JSON."""

from pathlib import Path

from json_store import load_json, save_json
from models import Conference, Section, Student, Talk


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
