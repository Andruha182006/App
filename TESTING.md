# Тестування

## Швидкий старт

```powershell
# 1. Підняти тестовий PostgreSQL (порт 5433, окремий від основного)
docker compose -f docker-compose.test.yml up -d

# 2. Запустити всі тести
.\.venv\Scripts\python.exe -m pytest
```

Очікуваний результат: `162 passed`, покриття ~99%.

Після роботи:

```powershell
docker compose -f docker-compose.test.yml down
```

## Як це працює

- На старті тестової сесії створюється база `postgres_test` (якщо існує — перестворюється).
- Схема створюється через `Base.metadata.create_all`.
- Після кожного тесту всі таблиці очищуються `TRUNCATE ... RESTART IDENTITY CASCADE`.
- Після завершення сесії база видаляється.
- Unit-тести (`tests/unit`) не звертаються до БД взагалі.

## Запуск окремих частин

```powershell
.\.venv\Scripts\python.exe -m pytest tests/unit        # без БД
.\.venv\Scripts\python.exe -m pytest tests/api         # з PostgreSQL
.\.venv\Scripts\python.exe -m pytest tests/api/test_auth.py -v
.\.venv\Scripts\python.exe -m pytest -k "student" -x
```

## Покриття

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=api --cov=core --cov=models --cov=repository --cov=schemas --cov=services --cov-report=term-missing
```

## Використання власного PostgreSQL

За замовчуванням тести йдуть на `127.0.0.1:5433`, користувач `postgres`, пароль `postgres`, БД `postgres_test`.
Можна перевизначити змінними оточення:

```powershell
$env:TEST_POSTGRES_PORT = "5432"
$env:TEST_POSTGRES_PASSWORD = "ваш_пароль"
$env:TEST_POSTGRES_DB = "postgres_test"
.\.venv\Scripts\python.exe -m pytest
```

Користувач має мати право `CREATE DATABASE` / `DROP DATABASE`.

## Важливо

- Тести не можна запускати паралельно (`pytest-xdist`) — вони використовують одну тестову БД.
- Потрібен PostgreSQL 13+.
- На Windows у `tests/conftest.py` використовується `SelectorEventLoop`, бо `psycopg` не працює з `ProactorEventLoop`.
