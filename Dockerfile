# 1. Использование официального базового образа Python
FROM python:3.11-slim

# 2. Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Установка системных зависимостей, необходимых для psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Создание рабочей директории в контейнере
WORKDIR /app

# 5. Копирование файла с зависимостями и их установка
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 6. Копирование всего остального кода проекта в рабочую директорию
COPY . /app/
