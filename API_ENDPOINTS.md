# API Endpoints Documentation

## Общая структура API

Все API маршруты находятся под префиксом `/api/`

## Аутентификация

### JWT Token
- **POST** `/api/auth/token/` - получение JWT токена
- **POST** `/api/auth/token/refresh/` - обновление JWT токена
- **POST** `/api/auth/register/` - регистрация нового пользователя

## Курсы (Courses)

### ViewSet маршруты (рекомендуется)
- **GET** `/api/materials/courses/` - список всех курсов
- **POST** `/api/materials/courses/` - создание нового курса
- **GET** `/api/materials/courses/{id}/` - получение курса по ID
- **PUT** `/api/materials/courses/{id}/` - полное обновление курса
- **PATCH** `/api/materials/courses/{id}/` - частичное обновление курса
- **DELETE** `/api/materials/courses/{id}/` - удаление курса

### Дополнительные действия ViewSet
- **GET** `/api/materials/courses/{id}/lessons/` - получение всех уроков курса
- **POST** `/api/materials/courses/{id}/enroll/` - запись на курс

### Generic Views маршруты (альтернатива)
- **GET** `/api/materials/courses/list/` - список курсов
- **POST** `/api/materials/courses/create/` - создание курса
- **GET** `/api/materials/courses/{id}/` - получение курса
- **PUT/PATCH** `/api/materials/courses/{id}/update/` - обновление курса
- **DELETE** `/api/materials/courses/{id}/delete/` - удаление курса

## Уроки (Lessons)

### Generic Views маршруты
- **GET** `/api/materials/lessons/` - список всех уроков
- **POST** `/api/materials/lessons/create/` - создание нового урока
- **GET** `/api/materials/lessons/{id}/` - получение урока по ID
- **PUT/PATCH** `/api/materials/lessons/{id}/update/` - обновление урока
- **DELETE** `/api/materials/lessons/{id}/delete/` - удаление урока

## Пользователи (Users)

### ViewSet маршруты
- **GET** `/api/users/` - список пользователей
- **POST** `/api/users/` - создание пользователя
- **GET** `/api/users/{id}/` - получение пользователя по ID
- **PUT** `/api/users/{id}/` - обновление пользователя
- **PATCH** `/api/users/{id}/` - частичное обновление пользователя
- **DELETE** `/api/users/{id}/` - удаление пользователя

### Профиль пользователя
- **GET** `/api/users/profile/` - получение профиля текущего пользователя
- **PUT** `/api/users/profile/` - полное обновление профиля
- **PATCH** `/api/users/profile/` - частичное обновление профиля

### Альтернативный способ через ViewSet
- **GET** `/api/users/profile/` - получение профиля
- **PUT** `/api/users/profile/` - обновление профиля
- **PATCH** `/api/users/profile/` - частичное обновление профиля

## Платежи (Payments)

### ViewSet маршруты
- **GET** `/api/payments/` - список платежей
- **POST** `/api/payments/` - создание платежа
- **GET** `/api/payments/{id}/` - получение платежа по ID
- **PUT** `/api/payments/{id}/` - обновление платежа
- **PATCH** `/api/payments/{id}/` - частичное обновление платежа
- **DELETE** `/api/payments/{id}/` - удаление платежа

## Права доступа

### Публичные маршруты (требуют только чтение)
- Список курсов
- Детали курса
- Список уроков
- Детали урока

### Защищенные маршруты (требуют аутентификации)
- Создание курса/урока
- Обновление курса/урока
- Удаление курса/урока
- Запись на курс
- **Редактирование профиля пользователя**

### Ограничения
- Пользователи могут редактировать только свои курсы и уроки
- **Пользователи могут редактировать только свой профиль**
- Администраторы имеют доступ ко всем данным

## Примеры использования

### Создание курса
```bash
POST /api/materials/courses/
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
    "title": "Python для начинающих",
    "description": "Базовый курс по Python",
    "preview": null
}
```

### Создание урока
```bash
POST /api/materials/lessons/create/
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
    "title": "Введение в Python",
    "description": "Первое занятие курса",
    "course": 1,
    "video_url": "https://example.com/video1.mp4"
}
```

### Получение уроков курса
```bash
GET /api/materials/courses/1/lessons/
Authorization: Bearer <your-jwt-token>
```

### Запись на курс
```bash
POST /api/materials/courses/1/enroll/
Authorization: Bearer <your-jwt-token>
```

### Обновление профиля пользователя
```bash
PATCH /api/users/profile/
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
    "first_name": "Александр",
    "last_name": "Петров",
    "phone": "+7 (999) 123-45-67",
    "city": "Москва"
}
```

### Получение профиля пользователя
```bash
GET /api/users/profile/
Authorization: Bearer <your-jwt-token>
```

## Коды ответов

- **200** - Успешный запрос
- **201** - Создано
- **400** - Ошибка валидации
- **401** - Не авторизован
- **403** - Доступ запрещен
- **404** - Не найдено
- **500** - Внутренняя ошибка сервера

## Заголовки

### Обязательные заголовки
- `Authorization: Bearer <jwt-token>` - для защищенных маршрутов
- `Content-Type: application/json` - для POST/PUT/PATCH запросов

### Опциональные заголовки
- `Accept: application/json` - для указания формата ответа

## Поля профиля пользователя

### Доступные для редактирования:
- `email` - электронная почта (уникальное)
- `username` - имя пользователя (уникальное)
- `first_name` - имя
- `last_name` - фамилия
- `phone` - телефон
- `city` - город
- `avatar` - аватарка (файл изображения)

### Только для чтения:
- `id` - идентификатор пользователя
- `date_joined` - дата регистрации
- `last_login` - последний вход
