# Документация компании (Docs-as-Code)

Внутренняя документация по проектам: техническая, вики и управленческая. Собрана с помощью **MkDocs + Material**, автогенерация API из docstrings — **mkdocstrings**, доступ по ссылке с **общим паролем**.

## Состав

- `mkdocs.yml` — конфигурация сайта и плагинов.
- `docs/` — содержимое (проекты, тех. документация, вики).
- `src/` — пример исходного кода с docstrings для mkdocstrings.
- `.github/workflows/deploy-docs.yml` — CI/CD на GitHub Pages.
- `mcp_server/` — MCP-сервер для управления документацией через ИИ.

## Быстрый старт (локально)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export DOCS_PASSWORD="dev-password"
mkdocs serve
```

Если пароль пустой — сайт открыт без пароля (для разработки).

## Автогенерация API из docstrings

В `docs/reference/python/example_pkg.md` блок `::: example_pkg` строит страницу из docstrings пакета в `src/`.

## Деплой на GitHub Pages

1. Репозиторий: `https://github.com/impossi8le/project-docs`.
2. В настройках репозитория: **Settings → Pages → Source: GitHub Actions**.
3. При пуше в `main` GitHub Actions собирает сайт и выкладывает на `https://impossi8le.github.io/project-docs/`.
4. Чтобы закрыть сайт паролем — задайте секрет `DOCS_PASSWORD`. Без секрета сайт открыт.

## MCP-сервер

MCP-сервер позволяет управлять документацией из диалога с ИИ.

Запуск:

```bash
python -m mcp_server.server
```

Подключение в Claude Desktop:

```json
{
  "mcpServers": {
    "docs-mcp": {
      "command": "python",
      "args": ["<путь>/mcp_server/server.py"]
    }
  }
}
```

Инструменты: `docs_list_projects`, `docs_list_pages`, `docs_read_page`, `docs_create_project_page`, `docs_write_page`, `docs_add_to_nav`, `docs_build`.
