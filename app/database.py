"""Модуль для работы с базой данных.

Содержит определения моделей SQLAlchemy, настройку подключения к БД 
и утилиты для работы с сессиями.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# URL для подключения к SQLite базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Создание движка SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Только для SQLite
)

# Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,  # Отключение авто-коммита
    autoflush=False,  # Отключение авто-сброса
    bind=engine  # Привязка к созданному движку
)

# Базовый класс для моделей
Base = declarative_base()

class User(Base):
    """Модель пользователя в базе данных.
    
    Attributes:
        id (int): Первичный ключ
        name (str): Имя пользователя (макс. 50 символов)
        surname (str): Фамилия пользователя (макс. 50 символов)
        tasks (relationship): Связь один-ко-многим с задачами пользователя
    """
    __tablename__ = "users"  # Название таблицы в БД

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    surname = Column(String(50))
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    """Модель задачи в базе данных.
    
    Attributes:
        id (int): Первичный ключ
        title (str): Заголовок задачи (макс. 100 символов)
        description (str, optional): Описание задачи
        created_at (datetime): Дата создания (автоматически при создании)
        updated_at (datetime): Дата обновления (автоматически при изменении)
        user_id (int): Внешний ключ к пользователю
        owner (relationship): Обратная связь многие-к-одному с пользователем
    """
    __tablename__ = "tasks"  # Название таблицы в БД

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, 
                      default=datetime.utcnow, 
                      onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")

def get_db():
    """Генератор сессий базы данных для использования в зависимостях FastAPI.
    
    Yields:
        Session: Сессия базы данных
        
    Note:
        Всегда закрывает сессию после завершения работы
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()