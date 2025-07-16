"""Pydantic модели для валидации данных и сериализации.

Этот модуль содержит все Pydantic модели, используемые для:
- Валидации входящих данных
- Сериализации исходящих данных
- Описания схем данных для API
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Базовая модель пользователя.
    
    Attributes:
        name (str): Имя пользователя
        surname (str): Фамилия пользователя
    """
    name: str
    surname: str


class UserCreate(UserBase):
    """Модель для создания пользователя.
    
    Наследует все поля от UserBase. Используется для валидации
    входящих данных при создании пользователя.
    """
    pass


class UserResponse(UserBase):
    """Модель ответа с данными пользователя.
    
    Attributes:
        id (int): Уникальный идентификатор пользователя
    """
    id: int
    
    class Config:
        """Конфигурация модели.
        
        Attributes:
            from_attributes (bool): Разрешает создание модели из ORM объекта
                                   (ранее known as orm_mode)
        """
        from_attributes = True


class TaskBase(BaseModel):
    """Базовая модель задачи.
    
    Attributes:
        title (str): Заголовок задачи
        description (Optional[str]): Описание задачи (опционально)
        user_id (int): ID пользователя, которому принадлежит задача
    """
    title: str
    description: Optional[str] = None
    user_id: int


class TaskCreate(TaskBase):
    """Модель для создания задачи.
    
    Наследует все поля от TaskBase. Используется для валидации
    входящих данных при создании задачи.
    """
    pass


class TaskUpdate(BaseModel):
    """Модель для обновления задачи.
    
    Attributes:
        title (Optional[str]): Новый заголовок задачи (опционально)
        description (Optional[str]): Новое описание задачи (опционально)
    """
    title: Optional[str] = None
    description: Optional[str] = None


class TaskResponse(BaseModel):
    """Модель ответа с данными задачи.
    
    Включает как данные задачи, так и информацию о пользователе.
    
    Attributes:
        id (int): Уникальный идентификатор задачи
        title (str): Заголовок задачи
        description (Optional[str]): Описание задачи
        created_at (datetime): Дата и время создания задачи
        updated_at (datetime): Дата и время последнего обновления задачи
        user_id (int): ID пользователя-владельца задачи
        user_name (str): Имя пользователя-владельца
        user_surname (str): Фамилия пользователя-владельца
    """
    id: int
    title: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    user_id: int  # Это поле обязательно
    user_name: str
    user_surname: str
    
    class Config:
        """Конфигурация модели.
        
        Attributes:
            from_attributes (bool): Разрешает создание модели из ORM объекта
                                   (ранее known as orm_mode)
        """
        from_attributes = True