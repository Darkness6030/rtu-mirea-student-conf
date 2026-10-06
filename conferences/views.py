from django.views.decorators.http import require_safe

from homepage.data import get_object, with_state
from homepage.ui import badge, card, combine, facts, grid, heading, link, page


@require_safe
@with_state
def conference_list(request, state):
    cards = grid(
        card(
            conf.event_date.strftime("%d.%m.%Y"),
            conf.name,
            conf.location,
            link("conferences:detail", "О конференции →", conf.id),
            badge(
                "Приём открыт" if conf.is_open() else "Приём завершён",
                "open" if conf.is_open() else "neutral",
            ),
        )
        for conf in sorted(state["conferences"], key=lambda c: c.event_date)
    )
    return page(
        "Конференции",
        combine(
            (
                heading(
                    "Календарь науки",
                    "Конференции",
                    "Выберите конференцию, чтобы узнать сроки подачи и направления исследований.",
                ),
                cards,
            )
        ),
        "conferences",
    )


@require_safe
@with_state
def conference_detail(request, state, conference_id):
    conf = get_object(state["conferences"], conference_id)
    sections = [section for section in state["sections"] if section.conference is conf]
    content = combine(
        (
            link("conferences:list", "← Конференции", css="back-link"),
            heading("Конференция", conf.name, conf.location),
            facts(
                (
                    ("Дата проведения", conf.event_date.strftime("%d.%m.%Y")),
                    ("Приём до включительно", conf.deadline.strftime("%d.%m.%Y")),
                    ("Статус", badge("Приём открыт" if conf.is_open() else "Приём завершён")),
                )
            ),
            heading("Направления", "Секции конференции", "Темы и лимиты докладов"),
            grid(
                card(
                    "Секция",
                    section.name,
                    f"Лимит докладов: {section.capacity}",
                    link("sections:detail", "Открыть секцию →", section.id),
                )
                for section in sections
            ),
        )
    )
    return page(conf.name, content, "conferences")
