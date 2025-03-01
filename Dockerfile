FROM python:3.10.12

# Установка необходимых пакетов (если нужно)
RUN apt-get update && apt-get install -y curl

# Копирование скрипта wait-for-it.sh в контейнер и выдача прав на выполнение
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Остальные команды для установки зависимостей и запуска приложения
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# Пример команды, ожидающей доступность базы данных
CMD ["wait-for-it.sh", "di_mebel_db:3306", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
