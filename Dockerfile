FROM python:3.7.2
# WORKDIR /code
RUN mkdir /code
COPY requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt --no-cache-dir
COPY /broker /code
COPY .env /code
WORKDIR /code
# ENV webhook https://b24-c6seuo.bitrix24.ru/rest/1/3w8ykqme3u3w0e6q/
# CMD [cd /brocker]
CMD ["python3", "manage.py", "runserver", "0:8000"]

# RUN mkdir /app

# # Скопировать с локального компьютера файл зависимостей
# # в директорию /app.
# COPY requirements.txt /app

# # Выполнить установку зависимостей внутри контейнера.
# RUN pip3 install -r /app/requirements.txt --no-cache-dir

# # Скопировать содержимое директории /api_yamdb c локального компьютера
# # в директорию /app.
# COPY api_yamdb/ /app

# # Сделать директорию /app рабочей директорией. 
# WORKDIR /app

# # Выполнить запуск сервера разработки при старте контейнера.
# CMD ["python3", "manage.py", "runserver", "0:8000"]