from django.shortcuts import render
from django.views.decorators.http import require_safe

from homepage.data import get_object, with_state
from services import active_talks, sort_sections


def section_context(state, section):
    count = len(active_talks(state, section))
    return {
        "section": section,
        "active_count": count,
        "is_open": section.conference.is_open(),
        "has_free_slot": section.has_free_slot(count),
    }


@require_safe
@with_state
def section_list(request, state):
    sections = [section_context(state, section) for section in sort_sections(state)]
    return render(request, "sections/section_list.html", {"sections": sections})


@require_safe
@with_state
def section_detail(request, state, section_id):
    section = get_object(state["sections"], section_id)
    context = section_context(state, section)
    context["talks"] = [talk for talk in state["talks"] if talk.section is section]
    return render(request, "sections/section_detail.html", context)
