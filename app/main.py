"""TODO List API.

Это FastAPI приложение для управления задачами (TODO list) с пользователями.
Позволяет создавать, читать, обновлять и удалять пользователей и их задачи.
"""

from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import Base, User, Task, engine, get_db
from shemas import UserCreate, UserResponse, TaskCreate, TaskUpdate, TaskResponse
import uvicorn

app = FastAPI(title="TODO List API", version="1.0.0")

# Создание таблиц при старте
@app.on_event("startup")
def startup():
    """Создает все таблицы в базе данных при запуске приложения."""
    Base.metadata.create_all(bind=engine)

def get_user_or_404(db: Session, user_id: int) -> User:
    """Получает пользователя по ID или возвращает 404 ошибку.
    
    Args:
        db: Сессия базы данных
        user_id: ID пользователя для поиска
        
    Returns:
        Объект пользователя если найден
        
    Raises:
        HTTPException: 404 если пользователь не найден
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user

def get_task_or_404(db: Session, task_id: int) -> Task:
    """Получает задачу по ID или возвращает 404 ошибку.
    
    Args:
        db: Сессия базы данных
        task_id: ID задачи для поиска
        
    Returns:
        Объект задачи если найден
        
    Raises:
        HTTPException: 404 если задача не найдена
    """
    task = db.query(Task).options(joinedload(Task.owner)).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    return task

# Эндпоинты для пользователей
@app.post("/users", 
          response_model=UserResponse, 
          status_code=status.HTTP_201_CREATED,
          summary="Создать нового пользователя",
          description="Создает нового пользователя с указанными именем и фамилией")
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """Создает нового пользователя в системе.
    
    Args:
        user: Данные для создания пользователя (UserCreate)
        db: Сессия базы данных (зависимость)
        
    Returns:
        Созданный пользователь (UserResponse)
    """
    db_user = User(name=user.name, surname=user.surname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Эндпоинты для задач
@app.post("/tasks",
          response_model=TaskResponse,
          status_code=status.HTTP_201_CREATED,
          summary="Создать новую задачу",
          description="Создает новую задачу с указанным заголовком и описанием")
async def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> TaskResponse:
    """Создает новую задачу для указанного пользователя.
    
    Args:
        task: Данные для создания задачи (TaskCreate)
        db: Сессия базы данных (зависимость)
        
    Returns:
        Созданная задача с информацией о пользователе (TaskResponse)
        
    Raises:
        HTTPException: 404 если пользователь не найден
    """
    # Проверяем существование пользователя
    user = get_user_or_404(db, task.user_id)
    
    # Создаем задачу
    db_task = Task(
        title=task.title,
        description=task.description,
        user_id=task.user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Формируем ответ
    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at,
        user_id=db_task.user_id,
        user_name=user.name,
        user_surname=user.surname
    )

@app.get("/tasks",
         response_model=List[TaskResponse],
         summary="Получить задачи пользователя",
         description="Возвращает список всех задач для указанного пользователя")
async def get_user_tasks(user_id: int, db: Session = Depends(get_db)) -> List[TaskResponse]:
    """Получает все задачи для указанного пользователя.
    
    Args:
        user_id: ID пользователя
        db: Сессия базы данных (зависимость)
        
    Returns:
        Список задач пользователя с информацией о пользователе
    """
    tasks = db.query(Task).options(joinedload(Task.owner)).filter(Task.user_id == user_id).all()
    return [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=task.user_id,
            user_name=task.owner.name,
            user_surname=task.owner.surname
        )
        for task in tasks
    ]

@app.get("/tasks/all",
         response_model=List[TaskResponse],
         summary="Получить все задачи",
         description="Возвращает список всех задач с информацией о пользователях")
async def get_all_tasks(db: Session = Depends(get_db)) -> List[TaskResponse]:
    """Получает все задачи в системе.
    
    Args:
        db: Сессия базы данных (зависимость)
        
    Returns:
        Список всех задач с информацией о пользователях
    """
    tasks = db.query(Task).options(joinedload(Task.owner)).all()
    return [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=task.user_id,
            user_name=task.owner.name,
            user_surname=task.owner.surname
        )
        for task in tasks
    ]

@app.get("/tasks/{task_id}",
         response_model=TaskResponse,
         summary="Получить задачу по ID",
         description="Возвращает информацию о конкретной задаче")
async def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    """Получает задачу по её ID.
    
    Args:
        task_id: ID задачи
        db: Сессия базы данных (зависимость)
        
    Returns:
        Информация о задаче с данными пользователя
        
    Raises:
        HTTPException: 404 если задача не найдена
    """
    task = get_task_or_404(db, task_id)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        created_at=task.created_at,
        updated_at=task.updated_at,
        user_id=task.user_id,
        user_name=task.owner.name,
        user_surname=task.owner.surname
    )

@app.put("/tasks/{task_id}",
         response_model=TaskResponse,
         summary="Обновить задачу",
         description="Обновляет информацию о задаче")
async def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)) -> TaskResponse:
    """Обновляет информацию о задаче.
    
    Args:
        task_id: ID задачи для обновления
        task_data: Новые данные для задачи
        db: Сессия базы данных (зависимость)
        
    Returns:
        Обновленная задача с информацией о пользователе
        
    Raises:
        HTTPException: 404 если задача не найдена
    """
    task = get_task_or_404(db, task_id)
    
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        created_at=task.created_at,
        updated_at=task.updated_at,
        user_id=task.user_id,
        user_name=task.owner.name,
        user_surname=task.owner.surname
    )

@app.delete("/tasks/{task_id}",
            status_code=status.HTTP_200_OK,
            summary="Удалить задачу",
            description="Удаляет задачу с указанным ID")
async def delete_task(task_id: int, db: Session = Depends(get_db)) -> dict:
    """Удаляет задачу по её ID.
    
    Args:
        task_id: ID задачи для удаления
        db: Сессия базы данных (зависимость)
        
    Returns:
        Сообщение об успешном удалении
        
    Raises:
        HTTPException: 404 если задача не найдена
    """
    task = get_task_or_404(db, task_id)
    db.delete(task)
    db.commit()
    return {"message": "Задача успешно удалена"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)