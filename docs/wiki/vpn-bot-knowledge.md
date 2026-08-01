# База знаний: VPN Telegram Bot

Справочные материалы, регламенты и инструкции по проекту.

## Разработка

### Как запустить локально

```bash
# Клонирование
git clone git@github.com:impossi8le/freebotvpn.git
cd freebotvpn

# Виртуальное окружение
python -m venv venv
source venv/bin/activate

# Зависимости
pip install -r requirements.txt

# Настройка .env
cp env.example .env
# Отредактируйте .env — укажите TELEGRAM_TOKEN, DB_* и т.д.

# Запуск бота
python bot1.py
```

### Docker Compose

```bash
docker-compose up -d
```

Поднимает три контейнера:
- **db** — MySQL 8.0 (порт 3306)
- **bot** — основной бот (автоперезапуск)
- **adminer** — веб-интерфейс БД (порт 8080)

### Обновление на сервере

```bash
ssh root@<сервер>
cd /var/www/vpnbotfree_r_usr/data/www/vpnbotfree.ru
git pull
# если есть изменения в зависимостях:
source venv/bin/activate
pip install -r requirements.txt
# перезапуск бота:
pkill -f bot1.py
python bot1.py &
```

## Типовые задачи

### Добавление нового VPN-сервера

1. Добавить сервер в БД (таблица `servers`, поля: code, name, region_display, host, user, password)
2. Настроить на сервере скрипты генерации OpenVPN-конфигураций
3. Проверить доступность через SSH
4. Сервер появится в списке выбора у пользователей

### Изменение цен

Отредактировать `includes/pricing.py`:

```python
PRICES = {
    30: 140,    # 30 дней
    90: 400,    # 90 дней
    180: 750,   # 180 дней
    360: 1300,  # 360 дней
}
```

### Добавление администратора

Добавить Telegram chat_id в `ADMIN_IDS` в `helpBot.py` и/или `admin_handler.py`:

```python
ADMIN_IDS = [377182640, 459236851, <новый_id>]
```

## Устранение неполадок

### Бот не отвечает

1. Проверить, запущен ли процесс: `ps aux | grep bot1.py`
2. Проверить `.env` — актуален ли `TELEGRAM_TOKEN`
3. Проверить логи: `tail -f bot.log`

### Ошибки базы данных

1. Проверить MySQL: `systemctl status mysql`
2. Проверить подключение: `mysql -u vpnusr -p`
3. В Docker: `docker-compose logs db`

### Не генерируются конфиги

1. Проверить n8n: `curl http://194.87.252.181:5678/health`
2. Проверить `GENERATE_CONFIG_API_URL` в `.env`
3. Проверить логи n8n

### Платежи не проходят

1. Проверить ЮKassa: актуальность `YOOKASSA_SECRET_KEY`
2. Временно включить тестовый режим: `PAYMENT_TEST_BYPASS_ENABLED=1`
3. Проверить `bot.log` на ошибки payment_handler

## Регламенты

### Работа с поддержкой

- Пользователь пишет боту поддержки (`helpBot.py`)
- Бот классифицирует обращение (AI-триаж)
- Администратор видит тикет, может ответить через `/reply`
- Вся переписка сохраняется в БД (таблицы `support_*`)
- Администратор может запросить Client360 — полную сводку по клиенту

### Выдача тестовых доступов

Тестовый режим платежей:

```python
PAYMENT_TEST_BYPASS_ENABLED=1
PAYMENT_TEST_BYPASS_CODE=ch8917
```

Код вводится в админ-панели при оплате. Только для администраторов.

### Мониторинг истечения подписок

Скрипт `scripts/notify_expiring_configs.py` проверяет конфиги за 7, 3 и 1 день до истечения. Уведомления отправляются:

- В Telegram (основной бот)
- На email (если привязан)

Запуск скрипта:

```bash
python scripts/notify_expiring_configs.py
```

## Ссылки

- **Репозиторий:** `https://github.com/impossi8le/freebotvpn`
- **Сервер:** `vpnbotfree.ru` (root)
- **Бот:** `https://t.me/free1vpnbot`
- **Группа:** `https://t.me/hulapka`
- **Платёжный шлюз:** ЮKassa (shop_id: 472651)
- **Криптоплатежи:** Cryptomus
- **SMTP:** `mail.commuspace.ru`
- **n8n:** `http://194.87.252.181:5678`