"""Інтеграційні тести реєстрації, логіну та /me."""

import jwt

from core.config import settings
from tests.factories import create_user


async def test_register_returns_201_without_password(client):
    response = await client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "password123"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert body["name"] == "Alice"
    assert body["is_active"] is True
    assert "password" not in body
    assert "hashed_password" not in body


async def test_register_duplicate_email_returns_400(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "password123",
    }

    assert (await client.post("/register", json=payload)).status_code == 201

    response = await client.post("/register", json=payload)

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


async def test_register_validates_password_length(client):
    response = await client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "short"},
    )

    assert response.status_code == 422


async def test_register_validates_email(client):
    response = await client.post(
        "/register",
        json={"name": "Alice", "email": "invalid", "password": "password123"},
    )

    assert response.status_code == 422


async def test_login_returns_jwt(client, db_session):
    user = await create_user(
        db_session, email="alice@example.com", password="password123"
    )

    response = await client.post(
        "/login",
        data={"username": user.email, "password": "password123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"

    payload = jwt.decode(
        body["access_token"], settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert payload["sub"] == str(user.id)


async def test_login_wrong_password_returns_401(client, db_session):
    user = await create_user(db_session, email="alice@example.com", password="password123")

    response = await client.post(
        "/login",
        data={"username": user.email, "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


async def test_login_unknown_email_returns_401(client):
    response = await client.post(
        "/login",
        data={"username": "ghost@example.com", "password": "password123"},
    )

    assert response.status_code == 401


async def test_login_inactive_user_returns_400(client, db_session):
    user = await create_user(
        db_session, email="alice@example.com", password="password123", is_active=False
    )

    response = await client.post(
        "/login",
        data={"username": user.email, "password": "password123"},
    )

    assert response.status_code == 400


async def test_login_requires_form_fields(client):
    response = await client.post("/login", data={"username": "alice@example.com"})

    assert response.status_code == 422


async def test_read_me_with_token(client, db_session):
    user = await create_user(db_session, email="alice@example.com", password="password123")
    login = await client.post(
        "/login", data={"username": user.email, "password": "password123"}
    )
    token = login.json()["access_token"]

    response = await client.get("/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["id"] == str(user.id)
    assert response.json()["email"] == user.email


async def test_read_me_without_token_returns_401(client):
    response = await client.get("/me")

    assert response.status_code == 401


async def test_read_me_with_invalid_token_returns_401(client):
    response = await client.get(
        "/me", headers={"Authorization": "Bearer definitely-not-a-jwt"}
    )

    assert response.status_code == 401
