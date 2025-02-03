import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Получаем данные из переменных окружения, определённых в docker-compose.yml
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "di_mebel_db")
DB_USER = os.getenv("DB_USER", "di_user")
DB_PASS = os.getenv("DB_PASS", "di_password")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
