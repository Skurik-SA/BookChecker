FROM python:3.13-slim

# Устанавливаем зависимости ОС (если нужны расширения)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем только зависимости, чтобы кешировать pip-инсталляцию
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Точка входа для dev: миграции + запуск dev-сервера
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
