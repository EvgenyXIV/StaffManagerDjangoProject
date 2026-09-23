#!/bin/bash

# КРОССПЛАТФОРМЕННЫЙ КОД

# Реализована логика выбора типа базы данных.
# Тип базы может быть задан в команде run при запуске docker (docker-compose):
# (флаги -e --env переопределяют заданные параметры окружения)
# docker-compose run -e DATABASE=postgres(или sqlite)

# Определение ОС
    # Для Windows подобных ОС
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "mingw64" || "$OSTYPE" == "cygwin" ]]; then
    echo "Windows like OS"
    export PATH="/c/Windows/System32:$PATH"
    export DB_PATH="C:/Users/EvgenyMINI_S/PythonProjects/DjangoSynergyProject/staffmanager/db.sqlite3"
    export APP_PATH="C:/Users/EvgenyMINI_S/PythonProjects/DjangoSynergyProject/staffmanager/staffmanager"
else
    # Для Linux/Mac
    if [[ "$OSTYPE" == "linux-gnu" ]]; then
        echo "Linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "MacOS"
    fi
    export DB_PATH="./db.sqlite3"
    export APP_PATH="."
fi

# # Значения переменных окружения по умолчанию
# POSTGRES_HOST="${POSTGRES_HOST:-db}"
# POSTGRES_PORT="${POSTGRES_PORT:-5432}"
# POSTGRES_USER="${POSTGRES_USER:-postgres}"
# POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-postgres}"
# POSTGRES_DB="${POSTGRES_DB:-StaffManager}"

# Функция ожидания PostgreSQL
wait_for_postgres() {                           # Функция ожидания PostgreSQL.
    if [[ "$DATABASE" == "postgres" ]]; then    # Если база данных PostgreSQL,
        echo "Ожидание PostgreSQL..."           # то выводится сообщение.
        # Пока не подключится к postgresql-client, идёт цикл. с паузой 1 сек.
        while ! pg_isready -h $SQL_HOST -U $SQL_USER; do                 # Если postgresql-client установлен в Dockerfile
        # while ! curl --silent --head --fail http://$SQL_HOST:5432; do   # Если curl установлен в Dockerfile
        # while ! nc -z $SQL_HOST 5432; do                                # Если postgresql-client, curl не установлены
            sleep 1
            echo "Ожидание PostgreSQL..."                                   # Отладочный вывод в консоли Docker
            echo "POSTGRES_HOST: "$SQL_HOST, "POSTGRES_PORT: "$SQL_PORT     # Отладочный вывод в консоли Docker
        done
        echo "POSTGRES_HOST: "$SQL_HOST, "POSTGRES_PORT: "$SQL_PORT         # Отладочный вывод в консоли Docker
        echo "PostgreSQL готов"
    fi
}

# Функция проверки наличия и создания пустой базы данных postgres в случае отсутствия.
create_db() {                             
    echo "Проверка наличия базы данных " $SQL_DATABASE
    if PGPASSWORD="$SQL_PASSWORD" psql -h "$SQL_HOST" -U "$SQL_USER" -c "SELECT 1 FROM pg_database WHERE datname = '$SQL_DATABASE'" | grep -q 1; then
        echo "База данных ", $SQL_DATABASE, " уже существует"
    else
        PGPASSWORD="$SQL_PASSWORD" psql -h "$SQL_HOST" -U "$SQL_USER" -c "CREATE DATABASE $SQL_DATABASE"
        if [ $? -eq 0 ]; then
            echo "База данных ", $SQL_DATABASE, " успешно создана"
        else
            echo "Ошибка создания базы данных ", $SQL_DATABASE
            exit 1
        fi
    fi
}


# Обработка SQLite
if [[ "$DATABASE" == "sqlite" ]]; then  # Если база данных SQLite,
    if [[ ! -f $DB_PATH ]]; then      # Если по адресу ($DB_PATH) файл (-f) базы данных не (!) существует,
        echo "База данных sqlite не существует, создание пустой базы данных "
        touch $DB_PATH                # то создаётся пустой файл db.sqlite3.
        chmod 666 $DB_PATH            # права на чтение и запись (666) для всех пользователей. (660 - только для владельца)
    else
        echo "База данных sqlite существует"
    fi
# Обработка PostgreSQL
elif [[ "$DATABASE" == "postgres" ]]; then  # Если база данных PostgreSQL,
    wait_for_postgres                       # Выполняется функция ожидания PostgreSQL.
    create_db                         # Выполняется функция проверки наличия и создания пустой базы данных в случае отсутствия.
fi

# Выполнение миграций
python manage.py migrate 

# Запуск команды, заданной в DOCKER-COMPOSE
#python manage.py runserver 0.0.0.0:8000
exec "$@"