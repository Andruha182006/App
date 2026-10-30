"""Юніт-тести для services.users.UserService."""

from uuid import uuid4

import pytest
from fastapi import HTTPException

from models.users import User
from schemas.users import UserCreate
from services.users import UserService


class FakeUserRepository:
    def __init__(self, existing: User | None = None):
        self.existing = existing
        self.created_with: dict | None = None

    async def get_by_email(self, db, email: str):
        return self.existing

    async def create(self, db, *, email: str, name: str, hashed_password: str) -> User:
        self.created_with = {
            "email": email,
            "name": name,
            "hashed_password": hashed_password,
        }
        return User(
            id=uuid4(),
            email=email,
            name=name,
            hashed_password=hashed_password,
            is_active=True,
        )


@pytest.fixture
def user_in() -> UserCreate:
    return UserCreate(name="Alice", email="alice@example.com", password="password123")


async def test_register_hashes_password_and_creates_user(monkeypatch, user_in):
    monkeypatch.setattr("services.users.get_password_hash", lambda pwd: f"hashed::{pwd}")
    repo = FakeUserRepository()
    service = UserService(repo)

    user = await service.register_user(object(), user_in)

    assert repo.created_with == {
        "email": "alice@example.com",
        "name": "Alice",
        # API ніколи не зберігає пароль у відкритому вигляді
        "hashed_password": "hashed::password123",
    }
    assert user.email == "alice@example.com"


async def test_register_duplicate_email_raises_400(user_in):
    repo = FakeUserRepository(
        existing=User(email=user_in.email, hashed_password="x", is_active=True)
    )
    service = UserService(repo)

    with pytest.raises(HTTPException) as exc_info:
        await service.register_user(object(), user_in)

    assert exc_info.value.status_code == 400
    assert "already exists" in exc_info.value.detail
    assert repo.created_with is None


async def test_authenticate_returns_token(monkeypatch, user_in):
    user = User(
        id=uuid4(),
        email=user_in.email,
        hashed_password="hashed-password",
        is_active=True,
    )
    repo = FakeUserRepository(existing=user)
    service = UserService(repo)

    verified: list[tuple[str, str]] = []

    def fake_verify(plain: str, hashed: str) -> bool:
        verified.append((plain, hashed))
        return True

    monkeypatch.setattr("services.users.verify_password", fake_verify)
    monkeypatch.setattr("services.users.create_access_token", lambda subject: "signed-token")

    token = await service.authenticate_user(
        object(), email=user_in.email, password=user_in.password
    )

    assert token == "signed-token"
    assert verified == [(user_in.password, "hashed-password")]


async def test_authenticate_unknown_email_raises_401(monkeypatch):
    service = UserService(FakeUserRepository(existing=None))

    with pytest.raises(HTTPException) as exc_info:
        await service.authenticate_user(object(), email="ghost@example.com", password="x")

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


async def test_authenticate_wrong_password_raises_401(monkeypatch):
    user = User(id=uuid4(), email="alice@example.com", hashed_password="hash", is_active=True)
    service = UserService(FakeUserRepository(existing=user))
    monkeypatch.setattr("services.users.verify_password", lambda plain, hashed: False)

    with pytest.raises(HTTPException) as exc_info:
        await service.authenticate_user(
            object(), email="alice@example.com", password="wrong"
        )

    assert exc_info.value.status_code == 401


async def test_authenticate_inactive_user_raises_400(monkeypatch):
    user = User(
        id=uuid4(),
        email="alice@example.com",
        hashed_password="hash",
        is_active=False,
    )
    service = UserService(FakeUserRepository(existing=user))
    monkeypatch.setattr("services.users.verify_password", lambda plain, hashed: True)
    monkeypatch.setattr(
        "services.users.create_access_token",
        lambda subject: pytest.fail("Не можна видавати токен неактивному користувачу"),
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.authenticate_user(
            object(), email="alice@example.com", password="password123"
        )

    assert exc_info.value.status_code == 400
