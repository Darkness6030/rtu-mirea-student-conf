from django.views.decorators.http import require_safe

from homepage.data import get_object, with_state
from homepage.ui import badge, card, combine, facts, grid, heading, link, page


@require_safe
@with_state
def student_list(request, state):
    content = combine(
        (
            heading(
                "Научное сообщество", "Студенты", "Авторы исследований и участники конференций"
            ),
            grid(
                card(
                    student.group,
                    student.name,
                    f"Докладов: {sum(t.student is student for t in state['talks'])}",
                    link("students:detail", "Доклады студента →", student.id),
                )
                for student in state["students"]
            ),
        )
    )
    return page("Студенты", content, "students")


@require_safe
@with_state
def student_detail(request, state, student_id):
    student = get_object(state["students"], student_id)
    talks = [talk for talk in state["talks"] if talk.student is student]
    content = combine(
        (
            link("students:list", "← Студенты", css="back-link"),
            heading("Участник конференций", student.name, student.group),
            facts((("Группа", student.group), ("Всего докладов", len(talks)))),
            heading("Исследования", "Доклады студента", "Поданные и отменённые заявки"),
            grid(
                card(
                    talk.section.name,
                    talk.title,
                    talk.abstract,
                    link("talks:detail", "Открыть доклад →", talk.id),
                    badge(talk.status),
                )
                for talk in talks
            ),
        )
    )
    return page(student.name, content, "students")
