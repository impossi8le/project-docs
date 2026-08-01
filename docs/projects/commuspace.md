# Commuspace.ru

> Статус: **эксплуатация** · Обновлено: 2026-08-01

## Обзор

Веб-сайт VPN-сервиса с покупками через веб-интерфейс. Состоит из фронтенда (HTML/JS) и бэкенда (Express.js + MySQL + Redis + очереди BullMQ).

**Домен:** `https://commuspace.ru`  
**Путь:** `/var/www/commuspace_r_usr58/data/www/commuspace.ru/`

## Фронтенд

Статические HTML-страницы, собранные Vite:

```
├── index.html         # Главная (SEO-оптимизирована)
├── about.html         # О проекте
├── contacts.html      # Контакты
├── reviews.html       # Отзывы
├── assets/            # Скомпилированные JS/CSS
├── robots.txt
├── sitemap.xml
└── .htaccess
```

## Бэкенд (Express.js)

**Стек:** Node.js, Express 4, MySQL (Sequelize ORM), Redis (BullMQ), JWT, ЮKassa, Nodemailer, SSH2

```
backend/
├── src/
│   ├── server.js              # Точка входа, инициализация
│   ├── app.js                 # Express-приложение (helmet, cors, routes)
│   ├── config/
│   │   ├── env.js             # Переменные окружения
│   │   ├── db.js              # Sequelize + MySQL
│   │   └── redis.js           # ioredis подключение
│   ├── models/
│   │   └── index.js           # Модели: User, Purchase, Server, TgCode и др.
│   ├── controllers/
│   │   ├── auth.controller.js      # Регистрация, верификация через Telegram
│   │   ├── catalog.controller.js   # Каталог продуктов и серверов
│   │   ├── purchase.controller.js  # Создание покупки через ЮKassa
│   │   ├── webhook.controller.js   # Webhook ЮKassa (подтверждение оплаты)
│   │   └── me.controller.js        # Профиль пользователя
│   ├── services/
│   │   ├── yookassa.service.js     # Интеграция с ЮKassa API v3
│   │   ├── telegram.service.js     # Отправка кодов через Telegram Gateway
│   │   ├── mailer.service.js       # Отправка конфигов по email
│   │   └── ssh.service.js          # SSH-команды на VPN-серверы
│   ├── utils/
│   │   └── pricing.js              # Цены и расчёты (как в Python-боте)
│   ├── queues/
│   │   └── index.js                # BullMQ очереди: telegram-code, purchase-delivery
│   ├── middlewares/
│   │   └── auth.middleware.js      # JWT-аутентификация
│   └── routes/
│       ├── index.js                # Сборка роутов
│       ├── auth.routes.js
│       ├── catalog.routes.js
│       ├── purchase.routes.js
│       ├── webhook.routes.js
│       └── me.routes.js
├── package.json
└── .env.example
```

## API

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/auth/register` | Регистрация (email + telegramUsername) |
| POST | `/api/auth/telegram/request-code` | Запрос кода в Telegram |
| POST | `/api/auth/telegram/verify-code` | Подтверждение кода → JWT |
| GET | `/api/catalog` | Продукты, цены, серверы |
| POST | `/api/purchases` | Создание покупки (Bearer token) |
| POST | `/api/webhooks/yookassa` | Webhook подтверждения оплаты |
| GET | `/api/me` | Профиль пользователя |

## Архитектура оплаты

1. Пользователь выбирает тариф на сайте → POST `/api/purchases`
2. Бэкенд создаёт платёж в ЮKassa → возвращает `confirmationUrl`
3. Пользователь оплачивает на стороне ЮKassa
4. ЮKassa отправляет webhook на `/api/webhooks/yookassa`
5. Webhook активирует подписку → ставит задачу в `purchase-delivery` очередь BullMQ
6. Worker генерирует конфиг через SSH на VPN-сервере → отправляет пользователю

## Связь с другими проектами

- Использует те же **цены и тарифы**, что и Telegram-бот (`freebotvpn`)
- Использует **ЮKassa** (те же shop_id, что и в `.env` бота)
- Генерирует **OpenVPN-конфиги** через SSH на тех же серверах
- **SMTP** — тот же почтовый сервер (`mail.commuspace.ru`)
- Связан с **n8n** через общие VPN-серверы