"""MCP-сервер для управления документацией MkDocs.

Позволяет ИИ-ассистентам управлять документацией:
- просматривать структуру и статус;
- создавать/редактировать страницы проектов;
- добавлять страницы в навигацию mkdocs.yml;
- собирать сайт локально.

Запуск:
    python -m mcp_server.server

Подключение в Claude Desktop через конфигурацию MCP.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
PROJECTS_DIR = DOCS_DIR / "projects"
MKDOCS_YML = ROOT / "mkdocs.yml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _list_md(dir_path: Path) -> list[str]:
    if not dir_path.exists():
        return []
    return sorted(
        _relative(p) for p in dir_path.rglob("*.md") if p.is_file()
    )


def _slugify(title: str) -> str:
    slug = re.sub(r"[^\w\- ]", "", title.lower()).strip().replace(" ", "-")
    return slug or "untitled"


def list_projects() -> list[dict[str, str]]:
    """Список страниц проектов в docs/projects/."""
    return [
        {"path": _relative(p), "name": p.stem}
        for p in PROJECTS_DIR.glob("*.md")
    ]


def list_pages() -> list[dict[str, str]]:
    """Список всех markdown-страниц документации."""
    return [
        {"path": rel, "name": Path(rel).stem}
        for rel in _list_md(DOCS_DIR)
    ]


def read_page(path: str) -> str:
    """Читает содержимое страницы по относительному пути."""
    full = (DOCS_DIR / path).resolve()
    if not full.is_relative_to(DOCS_DIR.resolve()):
        raise ValueError("Путь вне docs/")
    if not full.exists():
        raise FileNotFoundError(f"Страница не найдена: {path}")
    return _read(full)


def create_project_page(title: str, status: str = "В разработке") -> dict[str, str]:
    """Создаёт страницу проекта по шаблону."""
    slug = _slugify(title)
    path = PROJECTS_DIR / f"{slug}.md"
    if path.exists():
        raise FileExistsError(f"Страница уже существует: {_relative(path)}")

    date = __import__("datetime").date.today().isoformat()
    content = f"""# {title}

> Статус: **{status}** · Обновлено: {date}

## Обзор

Опишите здесь назначение проекта.

## Статус

- [ ] Задача 1
- [ ] Задача 2

## Техническая документация

- Раздел в разработке

## Регламенты и вики

- Раздел в разработке

## Встречи

| Дата | Тема | Решения |
|------|------|---------|
|      |      |         |

## Ссылки

- Репозиторий: `https://github.com/impossi8le/{slug}`
"""
    _write(path, content)
    return {"path": _relative(path), "created": _relative(path)}


def write_page(path: str, content: str) -> dict[str, str]:
    """Создаёт или перезаписывает страницу документации."""
    full = (DOCS_DIR / path).resolve()
    if not full.is_relative_to(DOCS_DIR.resolve()):
        raise ValueError("Путь вне docs/")
    _write(full, content)
    return {"path": _relative(full), "updated": _relative(full)}


def add_to_nav(path: str, title: str) -> dict[str, str]:
    """Добавляет страницу в nav в mkdocs.yml (под разделом 'Проекты')."""
    nav_path = path.replace("docs/", "", 1)
    block = f'      - "{title}": {nav_path}'
    config = _read(MKDOCS_YML)

    marker = "# --- авто-добавление проектов (mcp) ---"
    if marker in config:
        pattern = re.compile(rf"{re.escape(marker)}.*?(?=\n  - |\Z)", re.S)
        config = pattern.sub(marker + "\n" + block, config)
    else:
        insert_after = "  - Теги: tags.md"
        if insert_after in config:
            config = config.replace(
                insert_after,
                insert_after + "\n" + marker + "\n" + block,
                1,
            )
        else:
            config += "\n" + marker + "\n" + block

    _write(MKDOCS_YML, config)
    return {"added": nav_path, "title": title}


def build_site() -> dict[str, Any]:
    """Собирает сайт: mkdocs build."""
    result = subprocess.run(
        ["mkdocs", "build"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return {
        "success": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout[-3000:],
        "stderr": result.stderr[-3000:],
    }


def main() -> None:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        raise SystemExit(
            "Не установлен пакет 'mcp'. Выполните: pip install -r requirements.txt"
        )

    mcp = FastMCP("docs-mcp")

    mcp.add_tool(list_projects, name="docs_list_projects")
    mcp.add_tool(list_pages, name="docs_list_pages")
    mcp.add_tool(read_page, name="docs_read_page")
    mcp.add_tool(create_project_page, name="docs_create_project_page")
    mcp.add_tool(write_page, name="docs_write_page")
    mcp.add_tool(add_to_nav, name="docs_add_to_nav")
    mcp.add_tool(build_site, name="docs_build")

    mcp.run()


if __name__ == "__main__":
    main()
