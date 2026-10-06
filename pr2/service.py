"""Сценарии конференций на словарях и списках."""

from datetime import date

from validation import iso_date, positive, text, validate_state


def find_by_id(items: list[dict], item_id: int) -> dict:
    for item in items:
        if item["id"] == item_id:
            return item
    raise ValueError(f"Объект №{item_id} не найден")


def add(state: dict, collection: str, **fields) -> dict:
    items = state[collection]
    item = {"id": max((obj["id"] for obj in items), default=0) + 1, **fields}
    candidate = {**state, collection: [*items, item]}
    validate_state(candidate)
    items.append(item)
    return item


def add_conference(state, name, event_date, deadline, location):
    return add(
        state,
        "conferences",
        name=text(name),
        event_date=event_date,
        deadline=deadline,
        location=text(location),
    )


def add_student(state, name, group):
    return add(state, "students", name=text(name), group=text(group))


def add_section(state, name, conference_id, capacity):
    return add(
        state,
        "sections",
        name=text(name),
        conference_id=positive(conference_id),
        capacity=positive(capacity),
    )


def submit_talk(state, title, abstract, student_id, section_id, today=None):
    section = find_by_id(state["sections"], section_id)
    conference = find_by_id(state["conferences"], section["conference_id"])
    if (today or date.today()) > iso_date(conference["deadline"]):
        raise ValueError("Приём докладов завершён")
    return add(
        state,
        "talks",
        title=text(title),
        abstract=text(abstract),
        student_id=positive(student_id),
        section_id=positive(section_id),
        is_cancelled=False,
    )


def cancel_talk(state, talk_id):
    find_by_id(state["talks"], talk_id)["is_cancelled"] = True


def search_talks(state, query):
    return [item for item in state["talks"] if query.casefold() in item["title"].casefold()]


def filter_sections(state, min_capacity):
    return (item for item in state["sections"] if item["capacity"] >= min_capacity)


def sort_sections(state):
    return sorted(state["sections"], key=lambda item: (item["capacity"], item["id"]))
