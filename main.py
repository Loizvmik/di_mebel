from fastapi import FastAPI
import uvicorn

# Импортируем engine, чтобы можно было вызвать create_all
from database import engine,Base
# Роутер с эндпоинтами
from src.furniture.router import router 

# Создаём таблицы (если их нет) при старте
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Регистрируем роутеры
app.include_router(router)

# Точка входа при локальном запуске (без docker)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
