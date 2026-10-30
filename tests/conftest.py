"""Спільні фікстури для тестів.

Тести працюють на реальному PostgreSQL. Для ізоляції на старті сесії
створюється окрема база (за замовчуванням ``postgres_test`` на порту 5433),
а між тестами всі таблиці очищуються через TRUNCATE.

Запуск тестової БД:

    docker compose -f docker-compose.test.yml up -d

Перевизначити підключення можна змінними оточення:
    TEST_POSTGRES_SERVER, TEST_POSTGRES_PORT, TEST_POSTGRES_USER,
    TEST_POSTGRES_PASSWORD, TEST_POSTGRES_DB
"""

import asyncio
import os
import re
import selectors
import sys
from collections.abc import AsyncGenerator
from urllib.parse import quote_plus
from uuid import uuid4

# Важливо: змінні оточення мають бути виставлені ДО імпорту core.config,
# інакше Settings() впаде, якщо .env відсутній (наприклад, у CI).
os.environ.setdefault("POSTGRES_USER", "postgres")
os.environ.setdefault("POSTGRES_PASSWORD", "postgres")
os.environ.setdefault("POSTGRES_SERVER", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "test_db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-tests-only-0123456789abcdef")

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.database import Base, get_db
from core.security import create_access_token
import models  # noqa: F401  (реєструє всі таблиці в Base.metadata)
from main import app
from models.users import User


@pytest.fixture(scope="session")
def _asyncio_loop_factory():
    """На Windows psycopg не працює з ProactorEventLoop — використовуємо Selector."""
    if sys.platform == "win32":
        return lambda: asyncio.SelectorEventLoop(selectors.SelectSelector())
    return None


TEST_SERVER = os.getenv("TEST_POSTGRES_SERVER", "127.0.0.1")
TEST_PORT = os.getenv("TEST_POSTGRES_PORT", "5433")
TEST_USER = os.getenv("TEST_POSTGRES_USER", "postgres")
TEST_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD", "postgres")
TEST_DB_NAME = os.getenv("TEST_POSTGRES_DB", "postgres_test")

if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", TEST_DB_NAME):
    raise RuntimeError(f"Некоректна назва тестової БД: {TEST_DB_NAME!r}")

_TABLES = ", ".join(f'"{table.name}"' for table in Base.metadata.sorted_tables)


def _database_url(dbname: str) -> str:
    return (
        f"postgresql+psycopg://{quote_plus(TEST_USER)}:{quote_plus(TEST_PASSWORD)}"
        f"@{TEST_SERVER}:{TEST_PORT}/{dbname}"
    )


def _admin_engine():
    """Підключення до службової БД ``postgres`` для CREATE/DROP DATABASE."""
    return create_async_engine(_database_url("postgres"), isolation_level="AUTOCOMMIT")


_TERMINATE_CONNECTIONS = text(
    "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
    "WHERE datname = :db AND pid <> pg_backend_pid()"
)


@pytest.fixture(scope="session")
async def db_engine():
    """Створює чисту PostgreSQL-базу на всю тестову сесію."""
    admin = _admin_engine()
    try:
        async with admin.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except OperationalError as exc:
        await admin.dispose()
        pytest.exit(
            "Не вдалося підключитися до тестового PostgreSQL.\n"
            f"URL: {_database_url('postgres')}\n"
            "Запустіть тестову БД: docker compose -f docker-compose.test.yml up -d\n"
            f"Деталі: {exc}",
            returncode=1,
        )

    async with admin.connect() as conn:
        await conn.execute(_TERMINATE_CONNECTIONS, {"db": TEST_DB_NAME})
        await conn.execute(text(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"'))
        await conn.execute(text(f'CREATE DATABASE "{TEST_DB_NAME}"'))
    await admin.dispose()

    engine = create_async_engine(_database_url(TEST_DB_NAME), pool_pre_ping=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()
    admin = _admin_engine()
    async with admin.connect() as conn:
        await conn.execute(_TERMINATE_CONNECTIONS, {"db": TEST_DB_NAME})
        await conn.execute(text(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"'))
    await admin.dispose()


@pytest.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(
        bind=db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session

    # Очищуємо таблиці після кожного тесту, щоб тести не впливали один на одного.
    # TRUNCATE виконується після закриття сесії, тому відкритих транзакцій немає.
    async with db_engine.begin() as conn:
        await conn.execute(text(f"TRUNCATE TABLE {_TABLES} RESTART IDENTITY CASCADE"))


@pytest.fixture
async def anon_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP-клієнт без авторизації."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        try:
            yield db_session
        except Exception:
            # Після IntegrityError сесію треба відкотити, інакше вона
            # залишиться в стані PendingRollback.
            await db_session.rollback()
            raise

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as http_client:
        yield http_client

    app.dependency_overrides.clear()


@pytest.fixture
async def client(
    anon_client: AsyncClient,
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    """HTTP-клієнт із валідним Bearer-токеном.

    CRUD-роутери захищені авторизацією, тому більшість тестів мають
    працювати від імені активного користувача.
    """
    user = User(
        email=f"client-{uuid4().hex[:12]}@example.com",
        name="Test Client",
        hashed_password="not-used-in-tests",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    token = create_access_token(subject=user.id)
    anon_client.headers["Authorization"] = f"Bearer {token}"

    yield anon_client
