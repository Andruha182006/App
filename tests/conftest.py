"""Спільні фікстури для тестів.

Тести працюють на SQLite (in-memory), тому PostgreSQL не потрібен.
Інтеграційні тести піднімають ASGI-застосунок через httpx.AsyncClient,
а залежність get_db підміняється на тестову сесію.
"""

import os
from collections.abc import AsyncGenerator

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
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.pool import StaticPool


# Models використовують postgresql.UUID, який SQLite не вміє компілювати.
# Для тестів рендеримо його як CHAR(32) — значення зберігаються як hex-рядок.
@compiles(PG_UUID, "sqlite")
def _compile_pg_uuid_for_sqlite(type_, compiler, **kw) -> str:  # noqa: ARG001
    return "CHAR(32)"


from core.database import Base, get_db  # noqa: E402
import models  # noqa: E402,F401  (реєструє всі таблиці в Base.metadata)
from main import app  # noqa: E402


@pytest.fixture
async def db_engine():
    """Свіжий in-memory SQLite для кожного тесту."""
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

    # SQLite за замовчуванням не перевіряє зовнішні ключі.
    from sqlalchemy import event

    @event.listens_for(engine.sync_engine, "connect")
    def _enable_foreign_keys(dbapi_connection, _record):  # noqa: ARG001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(
        bind=db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP-клієнт до застосунку з підміненою БД."""

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
    async with AsyncClient(transport=transport, base_url="http://testserver") as http_client:
        yield http_client

    app.dependency_overrides.clear()
