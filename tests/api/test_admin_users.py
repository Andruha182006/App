"""Інтеграційні тести керування користувачами адміністратором."""

from core.enums import UserRole
from core.security import create_access_token
from tests.factories import create_user


async def test_admin_can_create_teacher(client):
    response = await client.post(
        "/admin/users",
        json={
            "name": "Teacher",
            "email": "teacher@example.com",
            "password": "password123",
            "role": "teacher",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "teacher@example.com"
    assert body["role"] == "teacher"
    assert body["is_active"] is True


async def test_admin_can_list_users(client, db_session):
    await create_user(db_session, email="listed@example.com")

    response = await client.get("/admin/users")

    assert response.status_code == 200
    assert any(
        item["email"] == "listed@example.com"
        for item in response.json()
    )


async def test_admin_can_change_role(client):
    created = await client.post(
        "/admin/users",
        json={
            "name": "Student",
            "email": "student@example.com",
            "password": "password123",
            "role": "student",
        },
    )
    user_id = created.json()["id"]

    response = await client.patch(
        f"/admin/users/{user_id}",
        json={"role": "teacher"},
    )

    assert response.status_code == 200
    assert response.json()["role"] == "teacher"


async def test_public_register_ignores_role(client):
    response = await client.post(
        "/register",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "password123",
            "role": "admin",
        },
    )

    assert response.status_code == 201
    assert response.json()["role"] == "student"


async def test_admin_endpoint_rejects_student(client, db_session):
    user = await create_user(
        db_session,
        email="student-token@example.com",
        role=UserRole.student,
    )
    client.headers["Authorization"] = (
        f"Bearer {create_access_token(subject=user.id)}"
    )

    response = await client.get("/admin/users")

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"


async def test_admin_endpoint_requires_authentication(anon_client):
    response = await anon_client.get("/admin/users")

    assert response.status_code == 401
