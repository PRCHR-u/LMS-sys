# API редактирования профиля пользователя

## Обзор

Реализован эндпоинт для редактирования профиля пользователя с возможностью частичного обновления данных.

## Эндпоинты

### 1. Получение профиля текущего пользователя

**GET** `/api/users/profile/`

**Описание**: Получение профиля текущего аутентифицированного пользователя

**Заголовки**:
```
Authorization: Bearer <jwt-token>
```

**Ответ** (200 OK):
```json
{
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "phone": "+7 (999) 123-45-67",
    "city": "Москва",
    "avatar": "http://example.com/media/avatars/user_avatar.jpg"
}
```

### 2. Обновление профиля (PUT)

**PUT** `/api/users/profile/`

**Описание**: Полное обновление профиля пользователя

**Заголовки**:
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Тело запроса**:
```json
{
    "first_name": "Новое имя",
    "last_name": "Новая фамилия",
    "phone": "+7 (999) 987-65-43",
    "city": "Санкт-Петербург"
}
```

**Ответ** (200 OK):
```json
{
    "email": "user@example.com",
    "username": "username",
    "first_name": "Новое имя",
    "last_name": "Новая фамилия",
    "phone": "+7 (999) 987-65-43",
    "city": "Санкт-Петербург",
    "avatar": null
}
```

### 3. Частичное обновление профиля (PATCH)

**PATCH** `/api/users/profile/`

**Описание**: Частичное обновление профиля пользователя

**Заголовки**:
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Тело запроса** (только изменяемые поля):
```json
{
    "city": "Новый город"
}
```

**Ответ** (200 OK):
```json
{
    "email": "user@example.com",
    "username": "username",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "phone": "+7 (999) 123-45-67",
    "city": "Новый город",
    "avatar": null
}
```

### 4. Обновление профиля через ViewSet (альтернативный способ)

**GET** `/api/users/profile/` - получение профиля
**PUT** `/api/users/profile/` - полное обновление
**PATCH** `/api/users/profile/` - частичное обновление

## Поля профиля

### Доступные для редактирования поля:
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

## Валидация

### Уникальность email и username
- При изменении email проверяется уникальность
- При изменении username проверяется уникальность
- Ошибка 400 Bad Request при дублировании

### Пример ошибки валидации:
```json
{
    "email": ["Пользователь с таким email уже существует."],
    "username": ["Пользователь с таким username уже существует."]
}
```

## Права доступа

- **Требуется аутентификация**: `IsAuthenticated`
- Пользователь может редактировать только свой профиль
- Администраторы имеют доступ ко всем профилям через админку

## Примеры использования

### Обновление только имени и фамилии
```bash
PATCH /api/users/profile/
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
    "first_name": "Александр",
    "last_name": "Петров"
}
```

### Обновление контактной информации
```bash
PUT /api/users/profile/
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
    "email": "newemail@example.com",
    "phone": "+7 (999) 111-22-33",
    "city": "Екатеринбург"
}
```

### Обновление аватара
```bash
PATCH /api/users/profile/
Authorization: Bearer <jwt-token>
Content-Type: multipart/form-data

avatar: [файл изображения]
```

## Коды ответов

- **200 OK** - профиль успешно обновлен
- **400 Bad Request** - ошибка валидации данных
- **401 Unauthorized** - не авторизован
- **403 Forbidden** - доступ запрещен
- **404 Not Found** - пользователь не найден

## Безопасность

- Все запросы требуют JWT токен
- Пользователь может редактировать только свой профиль
- Валидация уникальности email и username
- Защита от CSRF атак (Django REST Framework)

## Интеграция с фронтендом

### React/JavaScript пример:
```javascript
const updateProfile = async (profileData) => {
    try {
        const response = await fetch('/api/users/profile/', {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(profileData)
        });
        
        if (response.ok) {
            const updatedProfile = await response.json();
            console.log('Профиль обновлен:', updatedProfile);
        }
    } catch (error) {
        console.error('Ошибка обновления профиля:', error);
    }
};
```

### Python requests пример:
```python
import requests

def update_profile(token, profile_data):
    url = 'http://localhost:8000/api/users/profile/'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.patch(url, json=profile_data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Ошибка: {response.status_code}')
```
