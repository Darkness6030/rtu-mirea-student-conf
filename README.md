# Сервис организации студенческих конференций

Учебный проект ПР6 на Django 5.2. Сущности: конференция, студент, секция, доклад.
Секция относится к конференции, доклад связан со студентом и секцией.

## Запуск

Python 3.11 или новее:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Открыть http://127.0.0.1:8000/. На Windows: `.venv\Scripts\activate`.
База данных не нужна. Bootstrap, CSS, логотип и JavaScript хранятся локально.

## Использование

В браузере доступны главная страница, списки и карточки:

| URL | View-функции | Шаблоны приложения |
| --- | --- | --- |
| `/` | `index` | `homepage/index.html` |
| `/conferences/`, `/conferences/1/` | `conference_list`, `conference_detail` | `conferences/conference_*.html` |
| `/students/`, `/students/1/` | `student_list`, `student_detail` | `students/student_*.html` |
| `/sections/`, `/sections/1/` | `section_list`, `section_detail` | `sections/section_*.html` |
| `/talks/`, `/talks/1/` | `talk_list`, `talk_detail` | `talks/talk_*.html` |

Число в адресе — ID объекта. Неизвестный адрес возвращает 404.
Для демонстрации собственной страницы 404:
`DJANGO_DEBUG=0 python manage.py runserver --insecure`.
В PowerShell: `$env:DJANGO_DEBUG="0"`, затем `python manage.py runserver --insecure`.
Флаг `--insecure` нужен только для локальной раздачи CSS при выключенной отладке.

Создание записей, подача и отмена докладов выполняются через `python main.py`.
Меню также поддерживает поиск, фильтрацию и сортировку. Приём открыт до дедлайна
включительно; переполнение секции и повторная активная заявка запрещены.
Отмена сохраняет доклад в истории и освобождает место.

Данные загружаются из `data/sample.json`. Консоль сохраняет изменения
в `data/runtime.json`, после чего веб-страницы используют этот файл.
Повреждённый файл не перезаписывается; веб возвращает 503.
Хранилище рассчитано на одну работающую консоль. Другой путь можно задать через
`python main.py --data путь.json`, а для веба — переменной `CONFERENCE_DATA_FILE`.
ORM, формы и авторизация относятся к следующим практикам.

## Что изменилось в ПР6

Цепочка обработки: URL → view → контекст → шаблон → HTML.
Предметная модель, JSON, консоль и маршруты ПР5 сохранены. HTML полностью вынесен
из Python; `homepage/ui.py` и функция `page()` удалены. Все страницы вызывают `render()`.
Главная остаётся простой: заголовок, краткое описание и список разделов, без баннера.

- `templates/base.html` — общий документ, блоки `title` и `content`, CSS и JavaScript.
- `templates/includes/navigation.html` — общая навигация через `include`.
- `<приложение>/templates/<приложение>/` — страницы с `extends "base.html"`.
- `conferences/includes/conference_card.html` — карточка конференции.
- `talks/includes/talk_card.html` — карточка доклада для трёх разных страниц.
- Включаемые шаблоны статусов используют `if`; списки — `for` и `empty`.
- Фильтры `length`, `default`, `date` и `truncatewords` форматируют данные.
- Ссылки используют `{% url 'talks:detail' talk.id %}` и пространства имён приложений.
- `{% load static %}` и `{% static %}` подключают локальные ресурсы.

В `settings.py`: `DIRS = [BASE_DIR / "templates"]`, `APP_DIRS = True`.
Контекст содержит Python-объекты и подготовленные счётчики; проверки сроков и
лимитов остаются в Python. Автоматическое экранирование шаблонов включено.
Аннотация сокращается только в списке, а в карточке доклада показана целиком.

Собственные ресурсы находятся в `homepage/static/homepage/`:
`css/style.css`, `img/logo.svg`, `js/main.js`. JavaScript обновляет год в подвале;
без него остаётся год, выведенный сервером. Bootstrap и лицензия — в `static/vendor/`.

## Файлы и проверки

`main.py` — консоль; `models/` — четыре класса; `services.py` — операции;
`storage.py` и `validation.py` — JSON и проверки; `studentconf/` — настройки и URL;
`homepage/data.py` — загрузка данных и обработка ошибок; `tests/` — тесты.

```sh
pytest -q
flake8 .
python manage.py check
git log --oneline
```

64 теста: 46 сценариев ПР5 сохранены, добавлено 18 проверок шаблонов, контекста,
включаемых фрагментов, фильтров, пустых связанных списков и статических путей.
Браузером проверяются переходы, мобильное отображение, логотип и работа JavaScript.

## Материалы и Git

`docs/` — локальные методички; `results/` — локальный отчёт и ответы на вопросы.
Обе папки внесены в `.gitignore` и удалены из всей истории Git. Их содержимое
не поставляется с клоном репозитория. После очистки хеши прежних коммитов изменились.

Метки `PR1`, `PR2`, `PR3`, `PR5` сохраняют историю учебных этапов до упрощения.
ПР6 оформлена отдельными коммитами с префиксом `PR6:` и меткой `PR6`.
Репозиторий: https://github.com/Darkness6030/rtu-mirea-student-conf

Темы шаблонов раздела 04 отработаны локально. Выполнение упражнений Яндекс Практикума
и проекта «Блогикум» подтверждается отдельно в личном кабинете.
Справка: [шаблоны Django](https://docs.djangoproject.com/en/5.2/topics/templates/),
[теги и фильтры](https://docs.djangoproject.com/en/5.2/ref/templates/builtins/),
[статические файлы](https://docs.djangoproject.com/en/5.2/howto/static-files/).
