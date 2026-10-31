# StudyFlow API

Backend для навчального процесу: студенти, викладачі, курси, завдання, розклад і JWT-автентифікація.

**Стек:** Python 3.12, FastAPI, SQLAlchemy 2 (async), PostgreSQL 16, Alembic, Pydantic 2, Docker.

**Стан:** 199 тестів.

---

## Можливості

- CRUD для студентів, викладачів, курсів, завдань і розкладу.
- Ролі `admin`, `teacher`, `student` і перевірка власності записів.
- Адміністративне керування користувачами та ролями.
- Створення студента або викладача разом з акаунтом одним адмінським запитом.
- Прив’язка акаунта до профілю студента або викладача.
- Групи студентів і доступ до розкладу своєї групи.
- Здача завдання студентом і збереження відповіді.
- Усі захищені ендпоінти потребують `Authorization: Bearer <token>`.
- Реєстрація, логін і endpoint `GET /me`.
- Фільтрація та пагінація (`skip`, `limit`).
- Валідація вхідних даних через Pydantic.
- Зрозумілі помилки БД: дублікати та конфлікти FK → `409`.
- CORS для frontend-клієнтів.
- Міграції Alembic.
- Docker Compose для API та PostgreSQL.
- Окрема тестова PostgreSQL-база.
- Логування запитів і заголовок `X-Process-Time`.

---

## Швидкий старт (Docker)

Потрібен Docker Desktop.

1. Створіть `.env` із шаблону:

```powershell
Copy-Item .env.example .env
```

2. Відкрийте `.env` і замініть `SECRET_KEY` на власний випадковий рядок:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

3. Запустіть сервіси:

```powershell
docker compose up -d --build
```

4. Створіть першого адміністратора:

```powershell
docker compose exec api python scripts/create_admin.py `
  --email admin@example.com --name Administrator
```

Скрипт попросить пароль. Якщо користувач з таким email уже існує, він буде
підвищений до `admin` і активований.

5. Перевірте стан:

```powershell
docker compose ps
```

Після запуску доступні:

| Що | Адреса |
|---|---|
| API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Healthcheck | http://localhost:8000/health |
| OpenAPI | http://localhost:8000/api/v1/openapi.json |

Основна БД опублікована на хост-порті **5435**.

> Якщо порт 8000 зайнятий, зупиніть інший процес або змініть мапінг у
> `docker-compose.yml` на `"8001:8000"`.

Корисні команди:

```powershell
docker compose logs -f api      # логи API
docker compose down             # зупинити
docker compose down -v          # зупинити й видалити дані БД
```

Дані БД зберігаються у volume `app_postgres_data`. Команда `docker compose down`
їх не видаляє.

---

## Запуск локально

Потрібен PostgreSQL і Python 3.12+.

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Створіть `.env` (або скопіюйте `.env.example`) і застосуйте міграції:

```powershell
Copy-Item .env.example .env
alembic upgrade head
.\.venv\Scripts\python.exe scripts\create_admin.py `
  --email admin@example.com --name Administrator
uvicorn main:app --reload
```

Якщо локальний API підключається до PostgreSQL із Docker, використовуйте:

```env
POSTGRES_SERVER=127.0.0.1
POSTGRES_PORT=5435
```

---

## Змінні оточення

| Змінна | За замовчуванням | Опис |
|---|---|---|
| `POSTGRES_USER` | — | користувач PostgreSQL |
| `POSTGRES_PASSWORD` | — | пароль PostgreSQL |
| `POSTGRES_SERVER` | `localhost` | хост БД |
| `POSTGRES_PORT` | `5432` | порт БД |
| `POSTGRES_DB` | — | назва БД |
| `SECRET_KEY` | — | ключ підпису JWT |
| `ALGORITHM` | `HS256` | алгоритм JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | час життя токена |
| `SQL_ECHO` | `false` | логувати SQL-запити |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:5173` | дозволені origin через кому |

У Docker API завжди підключається до `db:5432`; зовнішній порт БД — `5435`.
Тестова БД працює окремо на порту `5433`.

---

## API

Публічні маршрути: `/`, `/health`, `/register`, `/login`, `/docs`, `/redoc`,
`/api/v1/openapi.json`.

Усі маршрути `/students`, `/teachers`, `/courses`, `/tasks`, `/schedules` і
`/me` потребують токена.

### Отримання токена

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

Далі передавайте токен у заголовку:

```http
Authorization: Bearer <access_token>
```

### Ролі та доступи

Публічний `/register` завжди створює користувача з роллю `student`. Роль
зберігається в БД і перевіряється на кожному запиті; даним із JWT про роль не
довіряємо.

| Дія | `admin` | `teacher` | `student` |
|---|---|---|---|
| Керування користувачами | повне | — | — |
| Студенти | повний CRUD | — | свій профіль `/students/me` |
| Викладачі | повний CRUD | свій профіль `/teachers/me` | — |
| Курси | повний CRUD | CRUD лише своїх | лише читання |
| Завдання | повний CRUD | CRUD лише своїх | лише свої та здача |
| Розклад | повний CRUD | лише свій | лише своєї групи |

Списки курсів, завдань і розкладу автоматично звужуються до дозволених
записів. Спроба звернутися до чужого запису повертає `403`.

### Прив’язка профілю

Щоб студент або викладач міг користуватися `/students/me` чи `/teachers/me`,
акаунт потрібно прив’язати до профілю. Це робить адміністратор:

```http
POST /students/
{
  "name": "Alice",
  "age": 20,
  "email": "alice@example.com",
  "group": "KN-21",
  "user_id": "<UUID користувача>"
}
```

```http
POST /teachers/
{
  "name": "Bob",
  "email": "bob@example.com",
  "department": "Math",
  "user_id": "<UUID користувача>"
}
```

Роль акаунта має відповідати типу профілю: `student` для студента,
`teacher` для викладача. Один акаунт можна прив’язати лише до одного профілю
відповідного типу.

### Створення студента або викладача одним запитом

Щоб не робити два запити вручну, адміністратор може створити акаунт і профіль
одразу.

Студент:

```http
POST /admin/students
{
  "name": "Alice",
  "age": 20,
  "email": "alice@example.com",
  "group": "KN-21",
  "password": "password123"
}
```

Викладач:

```http
POST /admin/teachers
{
  "name": "Bob",
  "email": "bob@example.com",
  "department": "Math",
  "password": "password123"
}
```

Обидва ендпоінти:

- створюють `User` із відповідною роллю та хешем пароля;
- створюють профіль і прив’язують його через `user_id`;
- виконують обидва INSERT в одній транзакції — при помилці відкочується все;
- повертають створений профіль із заповненим `user_id`;
- повертають `409`, якщо email уже зайнятий акаунтом або профілем.

Старі дворівневі маршрути `POST /admin/users` + `POST /students/` або
`POST /teachers/` залишаються доступними.

### Здача завдання

Студент здає лише своє завдання:

```http
POST /tasks/{task_id}/submit
{
  "answer": "Текст відповіді"
}
```

Після здачі `status` стає `submitted`, а `submitted_at` заповнюється.

### Ресурси

| Ресурс | Маршрути |
|---|---|
| Admin users | `GET/POST /admin/users`, `PATCH /admin/users/{user_id}` |
| Admin profiles | `POST /admin/students`, `POST /admin/teachers` |
| Students | `GET /students/me`; адмін: `GET/POST /students/`, `GET/PATCH/DELETE /students/{id}` |
| Teachers | `GET /teachers/me`; адмін: `GET/POST /teachers/`, `GET/PATCH/DELETE /teachers/{id}` |
| Courses | `GET/POST /courses/`, `GET/PATCH/DELETE /courses/{id}` |
| Tasks | `GET/POST /tasks/`, `GET/PATCH/DELETE /tasks/{id}`, `POST /tasks/{id}/submit` |
| Schedules | `GET/POST /schedules/`, `GET/PATCH/DELETE /schedules/{id}` |

### Фільтри та пагінація

```text
GET /students/?name=Alice
GET /courses/?teacher_id=1
GET /schedules/?group=KN-21
GET /students/?skip=0&limit=20
```

Обмеження: `skip >= 0`, `1 <= limit <= 100`.

Якщо фільтр нічого не знайшов, повертається `200` і порожній список `[]`.

### Помилки

- `401` — немає токена або токен недійсний.
- `403` — роль не має доступу або запис належить іншому користувачу.
- `404` — запис за id не знайдено.
- `409` — дублікат унікального поля, неіснуючий FK, невідповідна роль
  профілю або спроба видалити запис, на який посилаються інші дані.
- `422` — некоректні вхідні дані або параметри пагінації.

Видалення не робить каскад: якщо на запис є посилання, спочатку видаліть або
змініть залежні записи.

---

## Структура проєкту

```text
app/
├── api/v1/          # роутери та залежності
├── core/            # конфігурація, БД, безпека, middleware
├── models/          # SQLAlchemy-моделі
├── repository/      # доступ до даних
├── schemas/         # Pydantic-схеми
├── services/        # бізнес-логіка
├── scripts/         # службові команди (створення адміна)
├── alembic/         # міграції
├── tests/           # unit та API тести
├── main.py          # точка входу FastAPI
├── docker-compose.yml
├── docker-compose.test.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

Архітектура: `router → service → repository → database`.

---

## Міграції

```bash
alembic upgrade head
alembic downgrade -1
alembic revision --autogenerate -m "add something"
```

У Docker міграції виконуються автоматично під час старту контейнера `api`.

---

## Тести

Тести працюють на реальному PostgreSQL, не на SQLite.

```powershell
# 1. Підняти тестову БД
docker compose -f docker-compose.test.yml up -d

# 2. Запустити тести
.\.venv\Scripts\python.exe -m pytest
```

Очікуваний результат:

```text
199 passed
```

Окремі набори:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/unit
.\.venv\Scripts\python.exe -m pytest tests/api
.\.venv\Scripts\python.exe -m pytest tests/api/test_auth.py -v
```

Покриття:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  --cov=api --cov=core --cov=models --cov=repository `
  --cov=schemas --cov=services --cov=main --cov-report=term-missing
```

Детальніше — у [TESTING.md](TESTING.md).

Зупинити тестову БД:

```powershell
docker compose -f docker-compose.test.yml down
```

---

## Безпека

- Паролі зберігаються у вигляді Argon2-хешу.
- JWT підписується `SECRET_KEY` і містить `sub` та `exp`.
- Усі захищені роутери перевіряють підпис, термін дії токена й активність користувача.
- Роль береться з БД, а не з токена; для кожного запиту перевіряються роль і власність.
- Публічна реєстрація не дозволяє самостійно обрати роль.
- Вхідні дані перевіряються Pydantic.
- SQL-логування вимкнене за замовчуванням.
- Docker-контейнер API працює не від root.

> Для production згенеруйте новий `SECRET_KEY` і не зберігайте `.env` у Git.

---

## Що можна додати далі

- CI з автоматичним запуском тестів.
- Перевірку міграцій Alembic у тестах.
- Окремий `requirements-dev.txt`, щоб не ставити тестові залежності в production-образ.
- Поля дня тижня й часу в розкладі.

---

## Ліцензія

Навчальний проєкт.
