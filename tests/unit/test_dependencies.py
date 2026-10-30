"""Юніт-тести для api.v1.dependencies.get_current_user."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
import pytest
from fastapi import HTTPException

from api.v1 import dependencies
from core.config import settings
from core.security import create_access_token
from models.users import User


class FakeUserRepository:
    def __init__(self, user: User | None = None):
        self.user = user

    async def get_by_id(self, db, user_id):
        if self.user is not None and self.user.id == user_id:
            return self.user
        return None


@pytest.fixture
def active_user() -> User:
    return User(
        id=uuid4(),
        email="alice@example.com",
        hashed_password="hash",
        is_active=True,
    )


async def test_valid_token_returns_user(monkeypatch, active_user):
    monkeypatch.setattr(
        dependencies, "user_repository", FakeUserRepository(user=active_user)
    )
    token = create_access_token(subject=active_user.id)

    result = await dependencies.get_current_user(db=object(), token=token)

    assert result is active_user


async def test_unknown_user_raises_401(monkeypatch, active_user):
    monkeypatch.setattr(dependencies, "user_repository", FakeUserRepository(user=None))
    token = create_access_token(subject=active_user.id)

    with pytest.raises(HTTPException) as exc_info:
        await dependencies.get_current_user(db=object(), token=token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


async def test_inactive_user_raises_401(monkeypatch, active_user):
    active_user.is_active = False
    monkeypatch.setattr(
        dependencies, "user_repository", FakeUserRepository(user=active_user)
    )
    token = create_access_token(subject=active_user.id)

    with pytest.raises(HTTPException) as exc_info:
        await dependencies.get_current_user(db=object(), token=token)

    assert exc_info.value.status_code == 401


async def test_malformed_token_raises_401(monkeypatch):
    monkeypatch.setattr(dependencies, "user_repository", FakeUserRepository())

    with pytest.raises(HTTPException) as exc_info:
        await dependencies.get_current_user(db=object(), token="not-a-jwt")

    assert exc_info.value.status_code == 401


async def test_token_signed_with_wrong_key_raises_401(monkeypatch):
    monkeypatch.setattr(dependencies, "user_repository", FakeUserRepository())
    token = jwt.encode(
        {"sub": str(uuid4()), "exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        "wrong-secret",
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        await dependencies.get_current_user(db=object(), token=token)

    assert exc_info.value.status_code == 401


async def test_token_without_sub_raises_401(monkeypatch):
    monkeypatch.setattr(dependencies, "user_repository", FakeUserRepository())
    token = jwt.encode(
        {"exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        await dependencies.get_current_user(db=object(), token=token)

    assert exc_info.value.status_code == 401


async def test_non_uuid_sub_raises_401(monkeypatch):
    monkeypatch.setattr(dependencies, "user_repository", FakeUserRepository())
    token = jwt.encode(
        {
            "sub": "definitely-not-a-uuid",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        await dependencies.get_current_user(db=object(), token=token)

    assert exc_info.value.status_code == 401
