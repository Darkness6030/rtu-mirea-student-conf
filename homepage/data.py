"""Адаптер между Django и существующим хранилищем ПР3."""

import logging
from functools import wraps

from django.conf import settings
from django.http import Http404
from django.shortcuts import render

from services import find_by_id
from storage import load_state

logger = logging.getLogger(__name__)


def get_state():
    path = settings.DATA_FILE
    return load_state(path if path.exists() else settings.SAMPLE_FILE)


def get_object(items, item_id):
    try:
        return find_by_id(items, item_id)
    except ValueError as error:
        raise Http404("Объект не найден") from error


def with_state(view):
    """Читать свежий снимок один раз; не подменять повреждённый файл примером."""

    @wraps(view)
    def wrapped(request, *args, **kwargs):
        try:
            state = get_state()
        except (OSError, ValueError):
            logger.exception("Не удалось прочитать хранилище конференций")
            return render(request, "503.html", status=503)
        return view(request, state, *args, **kwargs)

    return wrapped
