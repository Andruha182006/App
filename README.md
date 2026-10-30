# StudyFlow API

API для управління навчальним процесом: студенти, викладачі, курси, завдання, розклад і автентифікація користувачів.

Побудований на FastAPI + SQLAlchemy 2 (async) + PostgreSQL, з JWT-автентифікацією, міграціями Alembic, Docker і тестами.

---

## Можливості

- CRUD для студентів, викладачів, курсів, завдань і розкладу
- Фільтрація та пагінація (`skip`, `limit`)
- Реєстрація та логін користувачів
- JWT-токени (PyJWT) і хешування паролів (Argon2)
- Захищений endpoint `GET /me`
- Асинхронна робота з PostgreSQL через SQLAlchemy 2 + psycopg
- Міграції Alembic
- Обробка конфліктів БД (дублікати, порушення FK) → HTTP 409
- Middleware для логування запитів і заголовка `X-Process-Time`
- Docker Compose для застосунку і БД
- 139 тестів, покриття ~98%

---

## Технології

| Технологія | Призначення |
|---|---|
| Python 3.12+ | мова |
| FastAPI | HTTP API |
| SQLAlchemy 2 (async) | ORM |
| PostgreSQL 16 | база даних |
| Alembic | міграції |
| Pydantic 2 | валідація та схеми |
| PyJWT | JWT-токени |
| pwdlib + Argon2 | хешування паролів |
| pytest + pytest-asyncio | тести |
| Docker Compose | запуск застосунку і БД |

---

## Структура проєкту

```
app/
├── api/v1/            # HTTP-роутери та залежності
│   ├── auth.py        # /register, /login
│   ├── users.py       # /me
│   ├── students.py
│   ├── teachers.py
│   ├── courses.py
│   ├── tasks.py
│   └── schedules.py
├── core/              # конфігурація, БД, безпека, middleware
├── models/            # SQLAlchemy-моделі
├── schemas/           # Pydantic-схеми
├── repository/        # доступ до даних
├── services/          # бізнес-логіка
├── alembic/           # міграції
├── tests/             # unit + API тести
├── main.py            # точка входу FastAPI
├── docker-compose.yml # основна БД + backend
├── docker-compose.test.yml # тестова БД для pytest
├── Dockerfile
└── requirements.txt
```

Архітектура: `router → service → repository → database`. Роутери не працюють з БД напряму, а викликають сервіси; сервіси — репозиторії.

---

## Швидкий старт (Docker)

Потрібен Docker Desktop.

```bash
docker compose up -d --build
```

Після запуску:

- API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- OpenAPI: <http://localhost:8000/api/v1/openapi.json>

Перевірити контейнери:

```bash
docker compose ps
```

Логи застосунку:

```bash
docker compose logs -f api
```

Зупинити:

```bash
docker compose down
```

> Дані БД зберігаються у volume `app_postgres_data` і не видаляються командою `down`.
> Щоб видалити і дані: `docker compose down -v`.

Після зміни коду перезберіть тільки backend:

```bash
docker compose up -d --build api
```

---

## Запуск локально (без Docker)

Потрібен запущений PostgreSQL.

1. Створіть віртуальне середовище та встановіть залежності:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS/WSL
# .\.venv\Scripts\activate     # Windows PowerShell
pip install -r requirements.txt
```

2. Створіть `.env` у корені проєкту:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=postgres_db

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

3. Застосуйте міграції:

```bash
alembic upgrade head
```

4. Запустіть сервер:

```bash
uvicorn main:app --reload
```

---

## Змінні оточення

| Змінна | За замовчуванням | Опис |
|---|---|---|
| `POSTGRES_USER` | — | користувач PostgreSQL |
| `POSTGRES_PASSWORD` | — | пароль |
| `POSTGRES_SERVER` | `localhost` | хост БД |
| `POSTGRES_PORT` | `5432` | порт БД |
| `POSTGRES_DB` | — | назва БД |
| `SECRET_KEY` | — | ключ для підпису JWT |
| `ALGORITHM` | `HS256` | алгоритм JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | час життя токена |

---

## API

Базовий префікс відсутній — маршрути доступні з кореня.

### Автентифікація

| Метод | Шлях | Опис |
|---|---|---|
| `POST` | `/register` | реєстрація |
| `POST` | `/login` | логін (form-data: `username`, `password`) |
| `GET` | `/me` | поточний користувач (Bearer token) |

### Ресурси

| Ресурс | Маршрути |
|---|---|
| Students | `GET/POST /students/`, `GET/PATCH/DELETE /students/{id}` |
| Teachers | `GET/POST /teachers/`, `GET/PATCH/DELETE /teachers/{id}` |
| Courses | `GET/POST /courses/`, `GET/PATCH/DELETE /courses/{id}` |
| Tasks | `GET/POST /tasks/`, `GET/PATCH/DELETE /tasks/{id}` |
| Schedules | `GET/POST /schedules/`, `PATCH/DELETE /schedules/{id}` |

Фільтри передаються query-параметрами, наприклад:

```
GET /students/?name=Alice
GET /courses/?teacher_id=1
GET /schedules/?group=KN-21
```

Пагінація:

```
GET /students/?skip=0&limit=20
```

---

## Міграції

```bash
alembic upgrade head                                  # застосувати
alembic downgrade -1                                  # відкотити одну
alembic revision --autogenerate -m "add something"    # створити нову
```

У Docker міграції виконуються автоматично при старті контейнера `api`.

---

## Тести

Тести використовують окрему PostgreSQL-базу (не SQLite).

1. Підніміть тестову БД:

```bash
docker compose -f docker-compose.test.yml up -d
```

2. Запустіть тести:

```bash
pytest
```

Очікуваний результат:

```
139 passed
```

Окремі набори:

```bash
pytest tests/unit                     # швидкі unit-тести, БД не потрібна
pytest tests/api                      # інтеграційні тести, потрібна тестова БД
pytest tests/api/test_auth.py -v      # один файл
pytest -k "student" -x                # за назвою, зупинитись на першій помилці
```

Покриття:

```bash
pytest --cov=api --cov=core --cov=models --cov=repository --cov=schemas --cov=services --cov-report=term-missing
```

Детальніше — у [TESTING.md](TESTING.md).

Зупинити тестову БД:

```bash
docker compose -f docker-compose.test.yml down
```

---

## Безпека

- Паролі зберігаються тільки у вигляді Argon2-хешу.
- JWT підписується `SECRET_KEY`; токен містить `sub` (id користувача) та `exp`.
- `GET /me` перевіряє підпис, термін дії токена та активність користувача.

> `SECRET_KEY` у прикладі — тестовий. Для реального середовища згенеруйте власний:
> `python -c "import secrets; print(secrets.token_urlsafe(64))"`.

---

## Плани розвитку

- Авторизація для CRUD-ендпоінтів (зараз вони відкриті)
- Ролі користувачів (`is_superuser`, викладач, студент)
- CI з автоматичним запуском тестів
- Docker-образ без dev-залежностей
- OpenAPI-документація з прикладами запитів

---

## Ліцензія

Навчальний проєкт.

