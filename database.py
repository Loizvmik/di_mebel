import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Получаем данные из переменных окружения, определённых в docker-compose.yml
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "di_mebel_db")
DB_USER = os.getenv("DB_USER", "admin_di_mebel")
DB_PASS = os.getenv("DB_PASS", "admin")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # Создаём базовый класс для всех моделей

def get_db():
    db = SessionLocal()
    try:
        yield db  # Передаём сессию в обработчик FastAPI
    finally:
        db.close()  # Закрываем сессию после запроса
