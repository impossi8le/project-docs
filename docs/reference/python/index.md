# Техническая документация

Здесь собрана автоматически генерируемая документация из docstrings вашего кода, а также техническая документация по проектам.

## Как это работает

Плагин **mkdocstrings** подхватывает docstrings прямо из исходного кода при каждой сборке.

## Поддерживаемые языки

Из коробки mkdocstrings умеет генерировать документацию для Python. Для TypeScript/JavaScript, C, Crystal, MATLAB, VBA и shell-скриптов нужны дополнительные обработчики.

## Как добавить страницу для модуля

В любом `.md` файле вставьте блок:

````markdown
::: имя.модуля
    options:
      show_root_heading: true
````

Путь к исходникам настраивается в `mkdocs.yml` в секции `plugins.mkdocstrings.handlers.python.paths`.

## Страницы

- [API (Python) — пакет example_pkg](example_pkg.md)
- [API (TypeScript) — example_ts](../typescript/example_ts.md)
- [VPN Bot — модули и API](vpn-bot/index.md) — полное описание всех модулей, хендлеров, утилит, API и админ-панели