from django.views.decorators.http import require_safe

from homepage.data import with_state
from homepage.ui import NAVIGATION, card, combine, grid, heading, link, page


@require_safe
@with_state
def index(request, state):
    content = combine(
        (
            heading(
                "СтудКонф",
                "Студенческие конференции",
                "Конференции, секции, участники и их доклады.",
            ),
            grid(
                card(label, str(len(state[name])), "", link(f"{name}:list", "Открыть →"))
                for name, label in NAVIGATION
            ),
        )
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
