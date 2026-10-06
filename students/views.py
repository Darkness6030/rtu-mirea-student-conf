from django.shortcuts import render
from django.views.decorators.http import require_safe

from homepage.data import get_object, with_state


@require_safe
@with_state
def student_list(request, state):
    students = [
        {"student": student, "talk_count": sum(t.student is student for t in state["talks"])}
        for student in state["students"]
    ]
    return render(request, "students/student_list.html", {"students": students})


@require_safe
@with_state
def student_detail(request, state, student_id):
    student = get_object(state["students"], student_id)
    talks = [talk for talk in state["talks"] if talk.student is student]
    return render(request, "students/student_detail.html", {"student": student, "talks": talks})
