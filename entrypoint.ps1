# Точка входа для среды Windows

# Реализована логика выбора типа базы данных.
# Тип базы может быть задан в команде run при запуске docker (docker-compose):
# (флаги -e --env переопределяют заданные параметры окружения)
# docker-compose run -e DATABASE=postgres(или sqlite)


# Если база POSTGRESQL
# Проверка переменной DATABASE (тип базы)
if ($env:DATABASE -eq "postgres") {       # 
    Write-Host "Ожидание PostgreSQL..."
    
    # Ожидание подключения к PostgreSQL
    while (-not (Test-NetConnection -ComputerName $env:HOST -Port 5432 -InformationLevel Quiet)) {
        Start-Sleep -Seconds 1
    }
    
    Write-Host "PostgreSQL запущен"
}

# Если база SQLITE3
# Проверяем тип базы данных
elseif ($env:DATABASE -eq "sqlite") {
    # Проверяем существование файла БД
    if (-not (Test-Path "/db.sqlite3")) {
        Write-Host "Создаем файл БД SQLite"
        New-Item -ItemType File -Name "db.sqlite3" -Path "/"
 }
} 

# Выполнение миграций Django
python manage.py flush --no-input
python manage.py migrate

# Выполнение переданной команды на запуск
& $args 