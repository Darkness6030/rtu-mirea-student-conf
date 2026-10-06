from django.views.decorators.http import require_safe

from homepage.data import get_object, with_state
from homepage.ui import badge, card, combine, facts, grid, heading, link, page
from services import active_talks, sort_sections


def section_status(state, section):
    if not section.conference.is_open():
        return badge("Приём завершён")
    if not section.has_free_slot(len(active_talks(state, section))):
        return badge("Мест нет", "cancelled")
    return badge("Есть места", "open")


@require_safe
@with_state
def section_list(request, state):
    content = combine(
        (
            heading(
                "Направления исследований",
                "Секции",
                "Найдите направление для своей работы. Секции упорядочены по лимиту докладов.",
            ),
            grid(
                card(
                    section.conference.name,
                    section.name,
                    f"Докладов: {len(active_talks(state, section))} / {section.capacity}",
                    link("sections:detail", "Открыть секцию →", section.id),
                    section_status(state, section),
                )
                for section in sort_sections(state)
            ),
        )
    )
    return page("Секции", content, "sections")


@require_safe
@with_state
def section_detail(request, state, section_id):
    section = get_object(state["sections"], section_id)
    talks = [talk for talk in state["talks"] if talk.section is section]
    content = combine(
        (
            link("sections:list", "← Секции", css="back-link"),
            heading("Секция", section.name, "Доклады и информация о приёме"),
            facts(
                (
                    (
                        "Конференция",
                        link("conferences:detail", section.conference.name, section.conference.id),
                    ),
                    (
                        "Подано / лимит",
                        f"{len(active_talks(state, section))} / {section.capacity}",
                    ),
                    ("Приём", section_status(state, section)),
                )
            ),
            heading("Программа секции", "Доклады", "Включая отменённые заявки"),
            grid(
                card(
                    talk.student.name,
                    talk.title,
                    talk.abstract,
                    link("talks:detail", "Открыть доклад →", talk.id),
                    badge(talk.status),
                )
                for talk in talks
            ),
        )
    )
    return page(section.name, content, "sections")
