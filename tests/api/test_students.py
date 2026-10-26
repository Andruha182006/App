"""Інтеграційні тести CRUD для /students."""

from tests.factories import create_student


async def test_create_student_returns_201(client):
    response = await client.post(
        "/students/",
        json={"name": "Alice", "age": 20, "email": "alice@example.com"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Alice"
    assert body["age"] == 20
    assert body["email"] == "alice@example.com"
    assert isinstance(body["id"], int)


async def test_create_student_validation_error(client):
    response = await client.post("/students/", json={"name": "Alice", "age": 20})

    assert response.status_code == 422


async def test_create_student_rejects_non_integer_age(client):
    response = await client.post(
        "/students/",
        json={"name": "Alice", "age": "twenty", "email": "alice@example.com"},
    )

    assert response.status_code == 422


async def test_create_student_with_duplicate_email_returns_409(client):
    payload = {"name": "Alice", "age": 20, "email": "duplicate@example.com"}

    assert (await client.post("/students/", json=payload)).status_code == 201

    response = await client.post("/students/", json=payload)

    assert response.status_code == 409


async def test_get_student_by_id(client, db_session):
    student = await create_student(db_session, name="Alice", age=20)

    response = await client.get(f"/students/{student.id}")

    assert response.status_code == 200
    assert response.json()["id"] == student.id


async def test_get_student_by_id_not_found(client):
    response = await client.get("/students/999")

    assert response.status_code == 404


async def test_list_students_empty(client):
    response = await client.get("/students/")

    assert response.status_code == 200
    assert response.json() == []


async def test_list_students_returns_all(client, db_session):
    await create_student(db_session, name="Alice")
    await create_student(db_session, name="Bob")

    response = await client.get("/students/")

    assert response.status_code == 200
    assert {item["name"] for item in response.json()} == {"Alice", "Bob"}


async def test_filter_students_by_name(client, db_session):
    await create_student(db_session, name="Alice")
    await create_student(db_session, name="Bob")

    response = await client.get("/students/", params={"name": "Alice"})

    assert response.status_code == 200
    assert [item["name"] for item in response.json()] == ["Alice"]


async def test_filter_students_by_name_not_found(client):
    response = await client.get("/students/", params={"name": "Nobody"})

    assert response.status_code == 404


async def test_filter_students_by_age(client, db_session):
    await create_student(db_session, name="Alice", age=20)
    await create_student(db_session, name="Bob", age=30)

    response = await client.get("/students/", params={"age": 30})

    assert response.status_code == 200
    assert [item["name"] for item in response.json()] == ["Bob"]


async def test_filter_students_by_email(client, db_session):
    student = await create_student(db_session, name="Alice")

    response = await client.get("/students/", params={"email": student.email})

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [student.id]


async def test_filter_students_by_unknown_email_returns_404(client):
    """Сервіс кидає 404, хоча endpoint очікує None і повертає []."""
    response = await client.get("/students/", params={"email": "ghost@example.com"})

    assert response.status_code == 404


async def test_filter_students_by_zero_age(client, db_session):
    await create_student(db_session, name="Baby", age=0)
    await create_student(db_session, name="Adult", age=20)

    response = await client.get("/students/", params={"age": 0})

    assert response.status_code == 200
    assert [item["name"] for item in response.json()] == ["Baby"]


async def test_pagination(client, db_session):
    for index in range(5):
        await create_student(db_session, name=f"Student{index}")

    response = await client.get("/students/", params={"skip": 1, "limit": 2})

    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_update_student_partial(client, db_session):
    student = await create_student(db_session, name="Alice", age=20)

    response = await client.patch(f"/students/{student.id}", json={"age": 21})

    assert response.status_code == 200
    body = response.json()
    assert body["age"] == 21
    assert body["name"] == "Alice"


async def test_update_student_not_found(client):
    response = await client.patch("/students/999", json={"age": 21})

    assert response.status_code == 404


async def test_delete_student(client, db_session):
    student = await create_student(db_session)

    response = await client.delete(f"/students/{student.id}")

    assert response.status_code == 204
    assert response.content == b""

    assert (await client.get(f"/students/{student.id}")).status_code == 404


async def test_delete_student_twice_returns_404(client, db_session):
    student = await create_student(db_session)

    assert (await client.delete(f"/students/{student.id}")).status_code == 204
    assert (await client.delete(f"/students/{student.id}")).status_code == 404
