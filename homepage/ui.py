"""Общие HTML-компоненты ПР5. Все значения из JSON экранируются."""

from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html, format_html_join

NAVIGATION = (
    ("conferences", "Конференции"),
    ("sections", "Секции"),
    ("talks", "Доклады"),
    ("students", "Студенты"),
)


def combine(parts):
    return format_html_join("", "{}", ((part,) for part in parts))


def link(route, label, item_id=None, css=""):
    url = reverse(route, args=[item_id] if item_id is not None else [])
    return format_html('<a class="{}" href="{}">{}</a>', css, url, label)


def badge(label, tone="neutral"):
    return format_html('<span class="status status-{}">{}</span>', tone, label)


def card(kicker, title, body, action, status=""):
    return format_html(
        '<article class="card item-card"><div class="card-body">'
        '<div class="card-top"><span class="eyebrow">{}</span>{}</div>'
        '<h2>{}</h2><p>{}</p><div class="card-action">{}</div></div></article>',
        kicker,
        status,
        title,
        body,
        action,
    )


def grid(cards, empty="Записей пока нет"):
    items = list(cards)
    if not items:
        return format_html('<p class="empty-state">{}</p>', empty)
    return format_html('<div class="cards-grid">{}</div>', combine(items))


def facts(rows):
    return format_html(
        '<dl class="facts">{}</dl>',
        format_html_join(
            "",
            "<div><dt>{}</dt><dd>{}</dd></div>",
            rows,
        ),
    )


def heading(kicker, title, description):
    return format_html(
        '<div class="page-heading"><p class="eyebrow">{}</p>'
        '<h1>{}</h1><p class="lead">{}</p></div>',
        kicker,
        title,
        description,
    )


def page(title, content, active="", status=200):
    navigation = combine(
        link(f"{name}:list", label, css="nav-link active" if name == active else "nav-link")
        for name, label in NAVIGATION
    )
    html = format_html(
        '<!doctype html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>{} · СтудКонф</title>"
        '<link rel="stylesheet" href="/static/vendor/bootstrap.min.css">'
        '<link rel="stylesheet" href="/static/site.css"></head><body>'
        '<a class="skip-link" href="#main">К содержимому</a>'
        '<header class="site-header"><div class="container header-inner">'
        '<a class="brand" href="/">СтудКонф</a>'
        '<nav aria-label="Основная навигация">{}</nav>'
        "</div></header>"
        '<main id="main" class="container">{}</main>'
        '<footer class="container site-footer"><span>СтудКонф · РТУ МИРЭА</span>'
        "</footer></body></html>",
        title,
        navigation,
        content,
    )
    return HttpResponse(html, status=status)
