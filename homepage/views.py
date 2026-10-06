from django.utils.html import format_html
from django.views.decorators.http import require_safe

from homepage.data import with_state
from homepage.ui import badge, card, combine, grid, heading, link, page


@require_safe
@with_state
def index(request, state):
    hero = format_html(
        '<section class="hero"><div class="hero-copy"><p class="eyebrow">'
        "Научное сообщество РТУ МИРЭА</p><h1>Большие идеи<br>начинаются здесь.</h1>"
        "<p>Студенческие конференции, новые исследования и люди, "
        "которые меняют будущее. Найдите свою секцию и познакомьтесь с докладами.</p>"
        '<div class="hero-actions">{} {}</div></div>'
        '<div class="hero-art" aria-hidden="true"><div class="orbit orbit-one"></div>'
        '<div class="orbit orbit-two"></div><span class="art-core">Наука<br>в движении</span>'
        '<span class="art-dot dot-one"></span><span class="art-dot dot-two"></span>'
        '<span class="art-label">ИДЕЯ → ИССЛЕДОВАНИЕ → ДОКЛАД</span></div></section>',
        link("conferences:list", "Смотреть конференции →", css="btn btn-primary"),
        link("talks:list", "Все доклады", css="btn btn-outline-dark"),
    )
    stats = format_html(
        '<section class="stats" aria-label="Сводка">{}</section>',
        combine(
            format_html("<div><strong>{}</strong><span>{}</span></div>", f"{count:02d}", label)
            for count, label in (
                (len(state["conferences"]), "конференции"),
                (len(state["sections"]), "секции"),
                (sum(not t.is_cancelled for t in state["talks"]), "активных доклада"),
                (len(state["students"]), "участника"),
            )
        ),
    )
    section_title = format_html(
        '<div class="section-heading"><div><p class="eyebrow">'
        "Календарь науки</p><h2>Конференции</h2></div>{}</div>",
        link("conferences:list", "Все конференции →"),
    )
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
    return page("Главная", combine((hero, stats, section_title, cards)))


def page_not_found(request, exception):
    content = combine(
        (
            heading(
                "Ошибка 404",
                "Страница не найдена",
                "Возможно, адрес изменился или запись больше не существует.",
            ),
            link("homepage:index", "На главную →", css="btn btn-primary"),
        )
    )
    return page("Страница не найдена", content, status=404)


def server_error(request):
    return page(
        "Ошибка сервера",
        heading("Ошибка 500", "Не удалось открыть страницу", "Попробуйте ещё раз позже."),
        status=500,
    )
