"""ПР3: пользовательские сценарии с объектами предметной области."""

from models import Conference, Section, Student, Talk
from validation import iso_date, text


def find_by_id(items: list, item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise ValueError(f"Объект №{item_id} не найден")


def next_id(items: list) -> int:
    return max((item.id for item in items), default=0) + 1


def add_conference(state, name, event_date, deadline, location):
    conference = Conference(
        next_id(state["conferences"]), name, iso_date(event_date), iso_date(deadline), location
    )
    state["conferences"].append(conference)
    return conference


def add_student(state, name, group):
    student = Student(next_id(state["students"]), name, group)
    state["students"].append(student)
    return student


def add_section(state, name, conference_id, capacity):
    section = Section(
        next_id(state["sections"]), name, find_by_id(state["conferences"], conference_id), capacity
    )
    state["sections"].append(section)
    return section


def active_talks(state, section):
    return [
        talk for talk in state["talks"] if talk.section.id == section.id and not talk.is_cancelled
    ]


def submit_talk(state, title, abstract, student_id, section_id, today=None):
    section = find_by_id(state["sections"], section_id)
    student = find_by_id(state["students"], student_id)
    title = text(title)
    if not section.conference.is_open(today):
        raise ValueError("Приём докладов завершён")
    active = active_talks(state, section)
    if any(
        talk.student.id == student_id and talk.title.casefold() == title.casefold()
        for talk in active
    ):
        raise ValueError("Повторная подача доклада")
    if not section.has_free_slot(len(active)):
        raise ValueError("Секция переполнена")
    talk = Talk(next_id(state["talks"]), title, abstract, student, section)
    state["talks"].append(talk)
    return talk


def cancel_talk(state, talk_id):
    find_by_id(state["talks"], talk_id).cancel()


def search_talks(state, query):
    return [talk for talk in state["talks"] if query.casefold() in talk.title.casefold()]


def filter_sections(state, min_capacity):
    return (section for section in state["sections"] if section.capacity >= min_capacity)


def sort_sections(state):
    return sorted(state["sections"], key=lambda section: (section.capacity, section.id))
