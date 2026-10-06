from django.shortcuts import render
from django.views.decorators.http import require_safe

from homepage.data import get_object, with_state


@require_safe
@with_state
def conference_list(request, state):
    conferences = sorted(state["conferences"], key=lambda item: item.event_date)
    return render(request, "conferences/conference_list.html", {"conferences": conferences})


@require_safe
@with_state
def conference_detail(request, state, conference_id):
    conference = get_object(state["conferences"], conference_id)
    sections = [section for section in state["sections"] if section.conference is conference]
    return render(
        request,
        "conferences/conference_detail.html",
        {
            "conference": conference,
            "sections": sections,
        },
    )
