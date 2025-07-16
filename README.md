Вот `README.md` для вашего проекта TODO List API:

```markdown
# TODO List API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1E4C67?style=for-the-badge&logo=sqlalchemy)

FastAPI приложение для управления задачами (TODO list) с пользователями. Позволяет создавать, читать, обновлять и удалять пользователей и их задачи.

## Особенности

- Создание и управление пользователями
- Создание, чтение, обновление и удаление задач (CRUD)
- Связь задач с пользователями
- Автоматическое создание таблиц при запуске
- Валидация данных
- Детальная документация API (Swagger UI)

## Требования

- Python 3.7+
- FastAPI
- SQLAlchemy
- Uvicorn

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/todo-list-api.git
   cd todo-list-api
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите приложение:
   ```bash
   uvicorn main:app --reload
   ```

Приложение будет доступно по адресу: `http://localhost:8000`


## Эндпоинты API

### Пользователи

- `POST /users` - Создать нового пользователя
  ```json
  {
    "name": "Иван",
    "surname": "Иванов"
  }
  ```

### Задачи

- `POST /tasks` - Создать новую задачу
  ```json
  {
    "title": "Новая задача",
    "description": "Описание задачи",
    "user_id": 1
  }
  ```

- `GET /tasks?user_id={user_id}` - Получить задачи пользователя
- `GET /tasks/all` - Получить все задачи
- `GET /tasks/{task_id}` - Получить задачу по ID
- `PUT /tasks/{task_id}` - Обновить задачу
  ```json
  {
    "title": "Обновленный заголовок",
    "description": "Обновленное описание"
  }
  ```

- `DELETE /tasks/{task_id}` - Удалить задачу

## Структура проекта

```
todo-list-api/
├── app/
|      |──main.py             # Основной файл приложения
|      ├── database.py         # Настройки базы данных и модели
|      ├── schemas.py         # Pydantic схемы для валидации
|── client.py            # Программа с клиентской частью 
|── README.md            # Документация
├── requirements.txt     # Зависимости
└── test.db              # База данных
```

## Примеры запросов

Создание пользователя:
```bash
curl -X POST "http://localhost:8000/users" \
-H "Content-Type: application/json" \
-d '{"name":"Иван","surname":"Иванов"}'
```

Создание задачи:
```bash
curl -X POST "http://localhost:8000/tasks" \
-H "Content-Type: application/json" \
-d '{"title":"Купить молоко","description":"2.5% жирности","user_id":1}'
```

Получение всех задач пользователя:
```bash
curl "http://localhost:8000/tasks?user_id=1"
```

