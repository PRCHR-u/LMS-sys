# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . /app/

# Собираем статические файлы
# Предполагается, что статика будет обрабатываться Nginx
# В docker-compose.yml мы создадим volume для статики
RUN python manage.py collectstatic --noinput

# Gunicorn будет слушать этот порт внутри контейнера
EXPOSE 8000

# Запускаем Gunicorn
# LMS-sys - это имя основной папки вашего Django проекта
CMD ["gunicorn", "LMS-sys.wsgi:application", "--bind", "0.0.0.0:8000"]
