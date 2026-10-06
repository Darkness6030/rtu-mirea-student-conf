from django.views.decorators.http import require_safe

from homepage.data import get_object, with_state
from homepage.ui import badge, card, combine, facts, grid, heading, link, page


@require_safe
@with_state
def talk_list(request, state):
    content = combine(
        (
            heading(
                "Студенческие исследования",
                "Доклады",
                "Темы, авторы и аннотации работ по всем конференциям",
            ),
            grid(
                card(
                    talk.section.name,
                    talk.title,
                    talk.student.name,
                    link("talks:detail", "Читать аннотацию →", talk.id),
                    badge(talk.status, "cancelled" if talk.is_cancelled else "open"),
                )
                for talk in state["talks"]
            ),
        )
    )
    return page("Доклады", content, "talks")


@require_safe
@with_state
def talk_detail(request, state, talk_id):
    talk = get_object(state["talks"], talk_id)
    content = combine(
        (
            link("talks:list", "← Доклады", css="back-link"),
            heading("Доклад", talk.title, talk.abstract),
            facts(
                (
                    ("Автор", link("students:detail", talk.student.name, talk.student.id)),
                    ("Секция", link("sections:detail", talk.section.name, talk.section.id)),
                    (
                        "Конференция",
                        link(
                            "conferences:detail",
                            talk.section.conference.name,
                            talk.section.conference.id,
                        ),
                    ),
                    ("Статус", badge(talk.status, "cancelled" if talk.is_cancelled else "open")),
                )
            ),
        )
    )
    return page(talk.title, content, "talks")
