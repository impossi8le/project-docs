# ИИ-документация компании (Docs-as-Code)

Внутренняя документация по проектам: техническая, вики и управленческая. Собрана с помощью **MkDocs + Material**, автогенерация API из docstrings — **mkdocstrings**. Доступ — открытая ссылка через GitHub Pages.

## Состав

- `mkdocs.yml` — конфигурация сайта и плагинов.
- `docs/` — содержимое (проекты, тех. документация, вики).
- `src/` — пример исходного кода с docstrings для mkdocstrings.
- `.github/workflows/deploy-docs.yml` — CI/CD на GitHub Pages.
- `mcp_server/` — MCP-сервер для управления документацией через ИИ.

## Быстрый старт (локально)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

mkdocs serve                      # http://localhost:8000
```

## Автогенерация API из docstrings

В `docs/reference/python/example_pkg.md` блок `::: example_pkg` автоматически строит страницу из docstrings пакета в `src/`. Пути к коду настраиваются в `mkdocs.yml`.

## Деплой на GitHub Pages

1. Репозиторий: `https://github.com/impossi8le/project-docs`.
2. В настройках репозитория: **Settings → Pages → Source: GitHub Actions**.
3. При пуше в `main` GitHub Actions собирает сайт и выкладывает на `https://impossi8le.github.io/project-docs/`.

## MCP-сервер

MCP-сервер позволяет управлять документацией из диалога с ИИ: просматривать страницы, создавать проекты, добавлять в навигацию, собирать сайт. Подробнее — в `mcp_server/`.

Альтернативно, документацией можно управлять напрямую через **GitHub MCP** — создавать/редактировать файлы в репозитории через GitHub API.

## Структура

```
docs/
├── index.md
├── projects/          # Страницы проектов
├── reference/         # Тех. документация (mkdocstrings)
├── wiki/              # Вики / база знаний
└── tags.md
src/example_pkg/       # Пример кода с docstrings
mcp_server/            # MCP-сервер
.github/workflows/     # CI/CD
```
