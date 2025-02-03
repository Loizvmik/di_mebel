# Используем официальный образ Python (можно заменить версию на нужную)
FROM python:3.10.12

# Указываем рабочую директорию внутри контейнера
WORKDIR /app

# Скопируем файл зависимостей
COPY requirements.txt .

# Установим все зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы проекта в контейнер
COPY . .

# Запуск сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
