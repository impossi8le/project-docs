# n8n Multi-Agent LLM Stack

> Статус: **эксплуатация** · Обновлено: 2026-08-01

## Обзор

Локальный multi-agent стек для оркестрации LLM-задач с автоматическим роутингом моделей. Использует n8n для графа workflow, собственный LLM Router для выбора модели и очередь Redis для worker-режима.

**Путь:** `/var/www/n8n_impossib_usr/data/www/n8n.impossible.com/`  
**Доступ:** `http://194.87.252.181:5678` (basic auth)

## Архитектура

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  n8n Main   │────▶│   Redis      │◀────│ n8n Worker  │
│  (webhooks) │     │  (очереди)   │     │ (execution) │
└──────┬──────┘     └──────────────┘     └──────┬──────┘
       │                                        │
       ▼                                        ▼
┌──────────────┐                       ┌──────────────┐
│ LLM Router   │                       │   Ollama     │
│ localhost:8090│                      │ localhost:11434│
│ FastAPI      │                       │ (локальные    │
│              │                       │  модели)     │
└──────┬───────┘                       └──────┬───────┘
       │                                      │
       ▼                                      ▼
┌──────────────┐                       ┌──────────────┐
│  PostgreSQL  │                       │   Qdrant     │
│ (n8n storage │                        │  localhost:6333│
│  + лог задач)│                       │ (векторная   │
└──────────────┘                       │  память)     │
                                       └──────────────┘
```

## Docker Compose (полный стек)

| Сервис | Образ | Порт | Назначение |
|--------|-------|------|------------|
| `postgres` | postgres:16 | — | Персистентность n8n + лог задач |
| `redis` | redis:7-alpine | — | Очереди BullMQ |
| `qdrant` | qdrant/qdrant | 6333 | Векторная база данных |
| `ollama` | ollama/ollama | 11434 | Локальные LLM (GPU) |
| `llm-router` | сборка из `router/` | 8090 | Роутинг задач по моделям |
| `n8n` | n8nio/n8n | 5678 | Оркестрация workflow |
| `n8n-worker` | n8nio/n8n | — | Исполнитель задач из очереди |
| `localtunnel` | efrecon/localtunnel | — | Туннель для вебхуков |

## LLM Router (FastAPI)

**Порт:** 8090  
**Стек:** FastAPI, httpx, qdrant-client, psycopg

### Модели (Ollama)

| Роль | Модель (primary) | Модель (secondary) |
|------|-----------------|-------------------|
| `router` | llama3.1:8b | qwen2.5:7b |
| `planning` | qwen2.5:14b | llama3.1:8b |
| `analysis` | qwen2.5:14b | llama3.1:8b |
| `coding` | codestral:22b | qwen2.5:14b |
| `qa` | llama3.1:8b | qwen2.5:7b |
| `chat` | llama3.1:8b | qwen2.5:7b |

### API

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/health` | Статус + GPU stats |
| `POST` | `/v1/route` | Определение модели под задачу |
| `POST` | `/v1/execute` | Полный цикл: выбор модели → выполнение → fallback |

### Fallback-цепочка

1. Primary локальная модель (Ollama)
2. Secondary локальная модель (Ollama)
3. Cloud fallback: `gpt-4.1-mini` (если `CLOUD_FALLBACK_ENABLED=true`)

### Память

- **Краткосрочная:** PostgreSQL (таблица `agent_runs`)
- **Семантическая:** Qdrant (коллекция `agent_memory`)
- **Тримминг контекста:** автоматическое усечение старых сообщений

## Инструмент submit_task.py

Отправка задач через CLI:

```bash
python tools/submit_task.py --type coding --prompt "Create a FastAPI project"
```

## Light-версия (без GPU)

`docker-compose.light.yml` — упрощённая версия без Ollama, Qdrant и n8n-worker. Включает только postgres, llm-router, localtunnel и n8n с лимитом памяти 600MB.

## Связь с другими проектами

- **n8n webhook** используется **Telegram-ботом (`freebotvpn`)** для генерации OpenVPN-конфигураций (`/webhook/generate-config`)
- **LLM Router** может быть использован для AI-классификации обращений в **helpBot.py** (support_classifier)
- **localtunnel** (`quiet-stingray-15.loca.lt`) используется для приёма вебхуков извне