"""Общие проверки и контракт JSON, независимые от интерфейса."""

from datetime import date

COLLECTIONS = ("conferences", "students", "sections", "talks")


def positive(value: int) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError("Ожидается положительное целое число")
    return value


def text(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Текст не может быть пустым")
    return value.strip()


def iso_date(value: str) -> date:
    if not isinstance(value, str):
        raise ValueError("Ожидается дата ГГГГ-ММ-ДД")
    result = date.fromisoformat(value)
    if result.isoformat() != value:
        raise ValueError("Ожидается дата ГГГГ-ММ-ДД")
    return result


def validate_state(state: dict) -> None:
    """Проверить поля, связи, уникальность и вместимость целого снимка."""
    if not isinstance(state, dict) or set(state) != set(COLLECTIONS):
        raise ValueError("Некорректные коллекции JSON")
    indexes = {}
    try:
        for name in COLLECTIONS:
            if not isinstance(state[name], list):
                raise ValueError("Коллекция должна быть списком")
            indexes[name] = {}
            for item in state[name]:
                if not isinstance(item, dict):
                    raise ValueError("Запись должна быть объектом")
                item_id = positive(item["id"])
                if item_id in indexes[name]:
                    raise ValueError("Повторяющийся идентификатор")
                indexes[name][item_id] = item
        for item in state["conferences"]:
            text(item["name"])
            text(item["location"])
            if iso_date(item["deadline"]) > iso_date(item["event_date"]):
                raise ValueError("Срок подачи позже конференции")
        for item in state["students"]:
            text(item["name"])
            text(item["group"])
        for item in state["sections"]:
            text(item["name"])
            positive(item["capacity"])
            indexes["conferences"][positive(item["conference_id"])]
        active = set()
        counts = {}
        for item in state["talks"]:
            text(item["title"])
            text(item["abstract"])
            student_id = positive(item["student_id"])
            section_id = positive(item["section_id"])
            indexes["students"][student_id]
            section = indexes["sections"][section_id]
            if type(item["is_cancelled"]) is not bool:
                raise ValueError("Статус должен иметь тип bool")
            if not item["is_cancelled"]:
                key = (student_id, section_id, item["title"].strip().casefold())
                if key in active:
                    raise ValueError("Повторная подача доклада")
                active.add(key)
                counts[section_id] = counts.get(section_id, 0) + 1
                if counts[section_id] > section["capacity"]:
                    raise ValueError("Секция переполнена")
    except (KeyError, TypeError) as error:
        raise ValueError("Отсутствующее поле или неверная ссылка в JSON") from error
