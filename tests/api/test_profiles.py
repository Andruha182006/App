"""Тести прив’язки акаунтів до профілів студента/викладача."""

from core.enums import UserRole
from tests.factories import create_user


async def test_admin_can_link_student_profile(client, db_session):
    user = await create_user(
        db_session,
        email="student-profile@example.com",
        role=UserRole.student,
    )

    response = await client.post(
        "/students/",
        json={
            "name": "Alice",
            "age": 20,
            "email": "alice@example.com",
            "group": "KN-21",
            "user_id": str(user.id),
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["group"] == "KN-21"
    assert body["user_id"] == str(user.id)


async def test_admin_can_link_teacher_profile(client, db_session):
    user = await create_user(
        db_session,
        email="teacher-profile@example.com",
        role=UserRole.teacher,
    )

    response = await client.post(
        "/teachers/",
        json={
            "name": "Bob",
            "department": "Math",
            "email": "bob@example.com",
            "user_id": str(user.id),
        },
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == str(user.id)


async def test_student_profile_requires_student_role(client, db_session):
    user = await create_user(
        db_session,
        email="admin-profile@example.com",
        role=UserRole.admin,
    )

    response = await client.post(
        "/students/",
        json={
            "name": "Alice",
            "age": 20,
            "email": "alice@example.com",
            "user_id": str(user.id),
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "User must have student role"


async def test_user_cannot_be_linked_to_two_students(client, db_session):
    user = await create_user(
        db_session,
        email="student-profile@example.com",
        role=UserRole.student,
    )
    payload = {
        "name": "Alice",
        "age": 20,
        "email": "alice@example.com",
        "user_id": str(user.id),
    }

    assert (await client.post("/students/", json=payload)).status_code == 201

    second = await client.post(
        "/students/",
        json={
            **payload,
            "email": "alice2@example.com",
        },
    )

    assert second.status_code == 409
    assert second.json()["detail"] == "User is already linked to another student"


async def test_student_can_read_own_profile(student_client):
    response = await student_client.get("/students/me")

    assert response.status_code == 200
    assert response.json()["group"] == "KN-21"


async def test_teacher_can_read_own_profile(teacher_client):
    response = await teacher_client.get("/teachers/me")

    assert response.status_code == 200
    assert response.json()["department"] == "Math"


async def test_student_cannot_read_teacher_profile(student_client):
    response = await student_client.get("/teachers/me")

    assert response.status_code == 403


async def test_teacher_cannot_read_student_profile(teacher_client):
    response = await teacher_client.get("/students/me")

    assert response.status_code == 403
