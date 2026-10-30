"""Інтеграційні тести CRUD для /teachers."""

from tests.factories import create_course, create_teacher


async def test_create_teacher_returns_201(client):
    response = await client.post(
        "/teachers/",
        json={"name": "Bob", "department": "Math", "email": "bob@example.com"},
    )

    assert response.status_code == 201
    assert response.json()["department"] == "Math"


async def test_create_teacher_validation_error(client):
    response = await client.post("/teachers/", json={"name": "Bob"})

    assert response.status_code == 422


async def test_get_teacher_by_id(client, db_session):
    teacher = await create_teacher(db_session)

    response = await client.get(f"/teachers/{teacher.id}")

    assert response.status_code == 200
    assert response.json()["id"] == teacher.id


async def test_get_teacher_not_found(client):
    response = await client.get("/teachers/999")

    assert response.status_code == 404


async def test_list_teachers(client, db_session):
    await create_teacher(db_session, name="Bob")
    await create_teacher(db_session, name="Carol")

    response = await client.get("/teachers/")

    assert response.status_code == 200
    assert {item["name"] for item in response.json()} == {"Bob", "Carol"}


async def test_filter_teachers_by_name(client, db_session):
    await create_teacher(db_session, name="Bob")
    await create_teacher(db_session, name="Carol")

    response = await client.get("/teachers/", params={"name": "Bob"})

    assert response.status_code == 200
    assert [item["name"] for item in response.json()] == ["Bob"]


async def test_filter_teachers_by_department(client, db_session):
    await create_teacher(db_session, department="Math")
    await create_teacher(db_session, department="Physics")

    response = await client.get("/teachers/", params={"department": "Physics"})

    assert response.status_code == 200
    assert [item["department"] for item in response.json()] == ["Physics"]


async def test_filter_teachers_by_email(client, db_session):
    teacher = await create_teacher(db_session)

    response = await client.get("/teachers/", params={"email": teacher.email})

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [teacher.id]


async def test_filter_teachers_by_name_not_found(client):
    response = await client.get("/teachers/", params={"name": "Nobody"})

    assert response.status_code == 200
    assert response.json() == []


async def test_filter_teachers_by_unknown_email_returns_empty(client):
    response = await client.get(
        "/teachers/", params={"email": "ghost@example.com"}
    )

    assert response.status_code == 200
    assert response.json() == []


async def test_create_teacher_rejects_invalid_email(client):
    response = await client.post(
        "/teachers/",
        json={
            "name": "Bob",
            "department": "Math",
            "email": "not-an-email",
        },
    )

    assert response.status_code == 422


async def test_update_teacher_with_full_payload(client, db_session):
    teacher = await create_teacher(db_session, name="Bob", department="Math")

    response = await client.patch(
        f"/teachers/{teacher.id}",
        json={"name": "Robert", "department": "Physics", "email": teacher.email},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Robert"
    assert response.json()["department"] == "Physics"


async def test_update_teacher_partial(client, db_session):
    teacher = await create_teacher(db_session, name="Bob")

    response = await client.patch(f"/teachers/{teacher.id}", json={"name": "Robert"})

    assert response.status_code == 200
    assert response.json()["name"] == "Robert"


async def test_update_teacher_not_found(client):
    response = await client.patch(
        "/teachers/999",
        json={"name": "Robert", "department": "Math", "email": "robert@example.com"},
    )

    assert response.status_code == 404


async def test_delete_teacher(client, db_session):
    teacher = await create_teacher(db_session)

    response = await client.delete(f"/teachers/{teacher.id}")

    assert response.status_code == 204
    assert (await client.get(f"/teachers/{teacher.id}")).status_code == 404


async def test_delete_teacher_with_course_returns_409(client, db_session):
    teacher = await create_teacher(db_session)
    await create_course(db_session, teacher=teacher)

    response = await client.delete(f"/teachers/{teacher.id}")

    assert response.status_code == 409
    assert "referenced" in response.json()["detail"]
