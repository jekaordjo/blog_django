# blog_djn

Блог о технологиях, Python и Django. Проект написан на Django с шаблонами. Статьи пишутся в Markdown через админку.

## Возможности

- Список статей с пагинацией, страницы рубрик и тегов.
- Страница статьи с подсветкой кода и переходом к соседним статьям.
- Черновики и дата публикации. Читатель видит только опубликованные статьи.
- Светлая и тёмная тема. Выбор сохраняется в браузере.
- Кнопка «Наверх».
- Bootstrap лежит в проекте. Внешние сервисы для стилей не нужны.
## Стек

- Python 3.14, Django 6.1, SQLite
- Bootstrap 5.3.9
- Markdown, Pygments, nh3 (разбор Markdown, подсветка кода, очистка HTML)
- uv, ruff, djlint, pre-commit
## Быстрый старт

1. Установите [uv](https://docs.astral.sh/uv/).
2. Скачайте проект и перейдите в его папку:
```bash
git clone <URL репозитория>
cd <папка проекта>
```

3. Установите зависимости:
```bash
uv sync
```

4. Создайте файл `.env` из примера:
```bash
cp .env.example .env
```

   В Windows: `copy .env.example .env`.

5. Создайте секретный ключ и вставьте его в `.env` в строку `SECRET_KEY`:
```bash
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

6. Создайте базу данных и администратора:
```bash
uv run manage.py migrate
uv run manage.py createsuperuser
```

7. Запустите сервер:
```bash
uv run manage.py runserver
```

Сайт: http://127.0.0.1:8000/. Админка: http://127.0.0.1:8000/admin/. Создайте в админке рубрику и статью со статусом «Опубликовано», чтобы статья появилась на сайте.

## Переменные окружения

- `SECRET_KEY` — секретный ключ Django. Не публикуйте его.
- `DEBUG` — режим отладки: `True` или `False`. Если переменная не задана, режим отладки выключен.
- `ALLOWED_HOSTS` — список разрешённых адресов через запятую, например `localhost,127.0.0.1`.
## Структура проекта

- `blog_djn/` — настройки и главные адреса проекта.
- `apps/blog/` — приложение блога: модели, view, адреса, админка.
- `templates/` — шаблоны.
- `static/` — стили, скрипты и Bootstrap.
## Разработка

Установите хуки pre-commit. Они проверяют код перед каждым коммитом:

```bash
uv run pre-commit install
```

Проверка вручную:

```bash
uv run ruff check .
uv run ruff format .
uv run djlint templates --check
uv run manage.py check
```

## Статус

Проект в разработке. Деплой пока не настроен.

## Лицензия

MIT. Текст лицензии в файле [LICENSE](LICENSE).
