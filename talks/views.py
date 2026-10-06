from django.shortcuts import render
from django.views.decorators.http import require_safe

from homepage.data import get_object, with_state


@require_safe
@with_state
def talk_list(request, state):
    return render(request, "talks/talk_list.html", {"talks": state["talks"]})


@require_safe
@with_state
def talk_detail(request, state, talk_id):
    talk = get_object(state["talks"], talk_id)
    return render(request, "talks/talk_detail.html", {"talk": talk})
