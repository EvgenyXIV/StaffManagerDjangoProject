# Базовый образ для Python
# https://hub.docker.com/_/python
FROM python:3.12-slim

# Устанавливаем рабочую директорию (после этого "." или "/staffmanager"- адреса рабочей директории в контейнере)
WORKDIR /usr/src/staffmanager/


# файлы .pyc могут содержать чувствительную информацию, 
# и их включение в образ может быть нежелательным.
# Запрещаем их копирование
ENV PYTHONDONTWRITEBYTECODE=1
# Запрещаем вывод stdout stderr вместо их настройки для логирования
# Так меньше ошибок и нет риска потери данных при удалении контейнера
ENV PYTHONUNBUFFERED=1

# Устанвливаем системные зависимости (curl, postgresql-client)
RUN apt-get update && \
    apt-get install -y \
    curl \
    postgresql-client

# Устанавливаем Python зависимости
# Сначала копируем requirements.txt из текущей диреткории проекта в рабочую директорию контейнера для кэширования
COPY ./requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip

# Параметр --no-cache-dir не указываем, кэширование (происходит по умолчанию) требуется.
# Это предохраняет от скачивания и установки обновлённых пакетов из репозитория,
# что может привести к проблемам с зависимостями.
RUN pip install -r requirements.txt

# Копирование файла скрипта из текущей папки вне проекта в рабочую папку контейнера для подключения к базе данных
# и созданию структуры БД по миграциям
COPY ./entrypoint.sh .

# На всякий случай, если в редакторе Windows изменялся файл, 
# то удаляем символы возврата каретки "\r" в конце строк для совместимости формата файла с Linux.
# Удаление знаков возврата каретки "\r" в конце строк (в среде windows \r\n, в Linux толко \n).
# Конвертация формата EOL (Windows -> Linux)
# Get-Content — читает содержимое файла
# Foreach-Object — обрабатывает каждую строку
# -replace — заменяет символы
# Set-Content — записывает изменённое содержимое обратно
# в среде Linux для совместимости после правки в Windows
RUN sed -i 's/\r$//g' /usr/src/staffmanager/entrypoint.sh

# Даём право запуска файла entrypoint.sh на исполнение в среде Docker-desctop (Linux)
RUN chmod +x /usr/src/staffmanager/entrypoint.sh

# Копируем все файлы проекта в рабочую директорию
COPY . .

# # Сборка статики (для продакшена)
# RUN python ./manage.py collectstatic --noinput

# Установка точки входа для запуска контейнера в файле entrypoint.sh
ENTRYPOINT ["/usr/src/staffmanager/entrypoint.sh"]
