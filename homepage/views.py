from django.shortcuts import render
from django.views.decorators.http import require_safe

from homepage.data import with_state


@require_safe
@with_state
def index(request, state):
    return render(request, "homepage/index.html", state)


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
