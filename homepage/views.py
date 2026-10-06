from django.utils.html import format_html, format_html_join
from django.views.decorators.http import require_safe

from homepage.data import with_state
from homepage.ui import NAVIGATION, combine, heading, link, page


@require_safe
@with_state
def index(request, state):
    content = format_html(
        '<h1 class="h4 mb-3">Студенческие конференции</h1><ul class="list-group">{}</ul>',
        format_html_join(
            "",
            '<li class="list-group-item d-flex justify-content-between">'
            '{}<span class="text-secondary">{}</span></li>',
            ((link(f"{name}:list", label), len(state[name])) for name, label in NAVIGATION),
        ),
    )
    return page("Главная", content)


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
