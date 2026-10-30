"""Інтеграційні тести CRUD для /courses."""

from tests.factories import create_course, create_teacher


async def test_create_course(client, db_session):
    teacher = await create_teacher(db_session)

    response = await client.post(
        "/courses/",
        json={"title": "Algebra", "credits": 5, "teacher_id": teacher.id},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Algebra"
    assert body["credits"] == 5
    assert body["teacher_id"] == teacher.id


async def test_create_course_validation_error(client):
    response = await client.post("/courses/", json={"title": "Algebra"})

    assert response.status_code == 422


async def test_create_course_with_unknown_teacher_returns_409(client):
    response = await client.post(
        "/courses/",
        json={"title": "Algebra", "credits": 5, "teacher_id": 999},
    )

    assert response.status_code == 409


async def test_get_course_by_id(client, db_session):
    course = await create_course(db_session)

    response = await client.get(f"/courses/{course.id}")

    assert response.status_code == 200
    assert response.json()["title"] == course.title


async def test_get_course_not_found(client):
    assert (await client.get("/courses/999")).status_code == 404


async def test_list_courses(client, db_session):
    await create_course(db_session, title="Algebra")
    await create_course(db_session, title="Physics")

    response = await client.get("/courses/")

    assert response.status_code == 200
    assert {item["title"] for item in response.json()} == {"Algebra", "Physics"}


async def test_filter_courses_by_title(client, db_session):
    await create_course(db_session, title="Algebra")
    await create_course(db_session, title="Physics")

    response = await client.get("/courses/", params={"title": "Physics"})

    assert response.status_code == 200
    assert [item["title"] for item in response.json()] == ["Physics"]


async def test_filter_courses_by_credits(client, db_session):
    await create_course(db_session, title="Algebra", credits=5)
    await create_course(db_session, title="Physics", credits=3)

    response = await client.get("/courses/", params={"credits": 3})

    assert response.status_code == 200
    assert [item["title"] for item in response.json()] == ["Physics"]


async def test_filter_courses_by_teacher_id(client, db_session):
    teacher = await create_teacher(db_session)
    other_teacher = await create_teacher(db_session)
    await create_course(db_session, title="Algebra", teacher=teacher)
    await create_course(db_session, title="Physics", teacher=other_teacher)

    response = await client.get("/courses/", params={"teacher_id": teacher.id})

    assert response.status_code == 200
    assert [item["title"] for item in response.json()] == ["Algebra"]


async def test_filter_courses_not_found(client):
    response = await client.get("/courses/", params={"title": "Nope"})

    assert response.status_code == 200
    assert response.json() == []


async def test_filter_courses_by_zero_credits(client, db_session):
    await create_course(db_session, title="Zero", credits=0)
    await create_course(db_session, title="Five", credits=5)

    response = await client.get("/courses/", params={"credits": 0})

    assert response.status_code == 200
    assert [item["title"] for item in response.json()] == ["Zero"]


async def test_create_course_rejects_negative_credits(client, db_session):
    teacher = await create_teacher(db_session)

    response = await client.post(
        "/courses/",
        json={"title": "Algebra", "credits": -1, "teacher_id": teacher.id},
    )

    assert response.status_code == 422


async def test_update_course_partial(client, db_session):
    course = await create_course(db_session, title="Algebra", credits=5)

    response = await client.patch(f"/courses/{course.id}", json={"credits": 6})

    assert response.status_code == 200
    assert response.json()["credits"] == 6
    assert response.json()["title"] == "Algebra"


async def test_update_course_not_found(client):
    response = await client.patch("/courses/999", json={"credits": 6})

    assert response.status_code == 404


async def test_delete_course(client, db_session):
    course = await create_course(db_session)

    response = await client.delete(f"/courses/{course.id}")

    assert response.status_code == 204
    assert (await client.get(f"/courses/{course.id}")).status_code == 404
