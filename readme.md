# BookChecker Backend

Для запуска

---

## 🔐 Переменные окружения

В корне проекта хранятся два файла с переменными:

### .env.dev
```dotenv
ENV=dev
DEBUG=True
SECRET_KEY='тут ключ'

POSTGRES_DB=bookshelf_dev
POSTGRES_USER=devuser
POSTGRES_PASSWORD=devpass

DB_HOST=db
DB_PORT=5432

YANDEX_SECRET=секретный ключ для яндекса
YANDEX_CLIENT_ID=ключ для пользователя
```

### .env.prod

Аналогичный по структуре, но с `DEBUG=False` и продакшен-значениями.

---

## 🚀 Разработка (dev)

1. Клонировать репозиторий и перейти в папку проекта:

   ```bash
   git clone <repo_url>
   cd <project_root>
   ```

2. Убедиться, что `.env.dev` присутствует и заполнен.

3. Запустить контейнеры:

   ```bash
   docker-compose up -d
   ```
   или если нужно собрать/пересобрать образы:
   ```bash
    docker-compose up -d --build
    ```

   В режиме разработки:

   * Код монтируется в контейнер,
   * Миграции применяются автоматически,
   * Dev-сервер Django запускается на `localhost:8000`.

---

## 👑 Админка

* URL: **`http://localhost:8000/admin/`**
* Доступ только для суперпользователя (создать его можно через `createsuperuser`).

```bash
    docker-compose exec web python manage.py createsuperuser
```
---

## 📖 Документация API

После старта проекта доступны:

* **OpenAPI schema**: `GET /api/schema/`
* **Swagger UI**:      `GET /api/docs/`
* **ReDoc**:           `GET /api/redoc/`

Очевидно по пути
* URL: **`http://localhost:8000/{один из путей выше}`**

---
Шпаргалка по командам `docker-compose`:

| Команда                                              | Описание                                            | Режим    |
| ---------------------------------------------------- | --------------------------------------------------- | -------- |
| `docker-compose up -d --build`                       | Собрать и запустить все сервисы (учтёт `override`)  | Dev      |
| `docker-compose -f docker-compose.yml up -d --build` | Собрать и запустить по чистому `docker-compose.yml` | Prod     |
| `docker-compose stop`                                | Остановить все контейнеры (даже в фоне)             | Dev/Prod |
| `docker-compose down`                                | Удалить контейнеры и сети, но **не** тома           | Dev/Prod |
| `docker-compose down -v`                             | Удалить контейнеры, сети и тома                     | Dev/Prod |
| `docker-compose ps`                                  | Показать статус всех сервисов                       | Dev/Prod |
| `docker-compose config`                              | Вывести итоговую конфигурацию (с учётом override)   | Dev/Prod |
| `docker-compose logs -f`                             | Смотреть логи всех сервисов в реальном времени      | Dev/Prod |
| `docker-compose logs web`                            | Смотреть только логи сервиса `web`                  | Dev/Prod |
| `docker-compose logs db`                             | Смотреть только логи сервиса `db`                   | Dev/Prod |
| `docker-compose build web`                           | Пересобрать образ сервиса `web`                     | Dev/Prod |
| `docker-compose build db`                            | Пересобрать образ сервиса `db`                      | Dev/Prod |
| `docker-compose pull`                                | Скачать свежие образы из реестра                    | Dev/Prod |
| `docker-compose restart web`                         | Перезапустить сервис `web`                          | Dev/Prod |
| `docker-compose restart db`                          | Перезапустить сервис `db`                           | Dev/Prod |