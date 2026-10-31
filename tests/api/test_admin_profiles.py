"""Інтеграційні тести створення студента/викладача разом з акаунтом."""

from sqlalchemy import func, select

from core.enums import UserRole
from models.users import User
from services.students import student_service
from tests.factories import create_student


async def test_admin_creates_student_with_account(client, db_session):
    response = await client.post(
        "/admin/students",
        json={
            "name": "Alice",
            "age": 20,
            "email": "alice-full@example.com",
            "group": "KN-21",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Alice"
    assert body["group"] == "KN-21"
    assert body["user_id"] is not None

    result = await db_session.execute(
        select(User).where(User.email == "alice-full@example.com")
    )
    user = result.scalar_one()
    assert user.role == UserRole.student
    assert str(user.id) == body["user_id"]

    login = await client.post(
        "/login",
        data={
            "username": "alice-full@example.com",
            "password": "password123",
        },
    )
    assert login.status_code == 200
    assert "access_token" in login.json()


async def test_admin_creates_teacher_with_account(client, db_session):
    response = await client.post(
        "/admin/teachers",
        json={
            "name": "Bob",
            "email": "bob-full@example.com",
            "department": "Math",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["department"] == "Math"
    assert body["user_id"] is not None

    result = await db_session.execute(
        select(User).where(User.email == "bob-full@example.com")
    )
    user = result.scalar_one()
    assert user.role == UserRole.teacher
    assert str(user.id) == body["user_id"]


async def test_admin_create_student_rejects_duplicate_user_email(
    client,
    db_session,
):
    payload = {
        "name": "Alice",
        "age": 20,
        "email": "duplicate@example.com",
        "group": "KN-21",
        "password": "password123",
    }

    first = await client.post("/admin/students", json=payload)
    second = await client.post("/admin/students", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == "User with this email already exists"

    count = await db_session.scalar(
        select(func.count())
        .select_from(User)
        .where(User.email == "duplicate@example.com")
    )
    assert count == 1


async def test_admin_create_student_rejects_existing_profile_email(
    client,
    db_session,
):
    await create_student(db_session, email="occupied@example.com")

    response = await client.post(
        "/admin/students",
        json={
            "name": "Alice",
            "age": 20,
            "email": "occupied@example.com",
            "group": "KN-21",
            "password": "password123",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Student with this email already exists"

    result = await db_session.execute(
        select(User).where(User.email == "occupied@example.com")
    )
    assert result.scalar_one_or_none() is None


async def test_admin_create_student_rolls_back_user_on_profile_conflict(
    client,
    db_session,
    monkeypatch,
):
    await create_student(db_session, email="race@example.com")

    async def missing_student(db, email):
        return None

    monkeypatch.setattr(
        student_service.repository,
        "get_by_email",
        missing_student,
    )

    response = await client.post(
        "/admin/students",
        json={
            "name": "Alice",
            "age": 20,
            "email": "race@example.com",
            "group": "KN-21",
            "password": "password123",
        },
    )

    assert response.status_code == 409
    result = await db_session.execute(
        select(User).where(User.email == "race@example.com")
    )
    assert result.scalar_one_or_none() is None


async def test_admin_create_student_requires_admin_role(student_client):
    response = await student_client.post(
        "/admin/students",
        json={
            "name": "Alice",
            "age": 20,
            "email": "forbidden@example.com",
            "group": "KN-21",
            "password": "password123",
        },
    )

    assert response.status_code == 403
