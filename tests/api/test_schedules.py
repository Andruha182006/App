"""Інтеграційні тести CRUD для /schedules."""

from tests.factories import create_course, create_schedule, create_teacher


async def test_create_schedule(client, db_session):
    teacher = await create_teacher(db_session)
    course = await create_course(db_session, teacher=teacher)

    response = await client.post(
        "/schedules/",
        json={
            "group": "KN-21",
            "room": 101,
            "course_id": course.id,
            "teacher_id": teacher.id,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["group"] == "KN-21"
    assert body["room"] == 101


async def test_create_schedule_validation_error(client):
    response = await client.post("/schedules/", json={"group": "KN-21"})

    assert response.status_code == 422


async def test_list_schedules(client, db_session):
    await create_schedule(db_session, group="KN-21")
    await create_schedule(db_session, group="KN-22")

    response = await client.get("/schedules/")

    assert response.status_code == 200
    assert {item["group"] for item in response.json()} == {"KN-21", "KN-22"}


async def test_filter_schedules_by_group(client, db_session):
    await create_schedule(db_session, group="KN-21")
    await create_schedule(db_session, group="KN-22")

    response = await client.get("/schedules/", params={"group": "KN-22"})

    assert response.status_code == 200
    assert [item["group"] for item in response.json()] == ["KN-22"]


async def test_filter_schedules_by_room(client, db_session):
    await create_schedule(db_session, room=101)
    await create_schedule(db_session, room=202)

    response = await client.get("/schedules/", params={"room": 202})

    assert response.status_code == 200
    assert [item["room"] for item in response.json()] == [202]


async def test_filter_schedules_by_course_id(client, db_session):
    teacher = await create_teacher(db_session)
    other_teacher = await create_teacher(db_session)
    course = await create_course(db_session, teacher=teacher)
    other_course = await create_course(db_session, teacher=other_teacher)
    await create_schedule(db_session, course=course, teacher=teacher)
    await create_schedule(db_session, course=other_course, teacher=other_teacher)

    response = await client.get("/schedules/", params={"course_id": course.id})

    assert response.status_code == 200
    assert [item["course_id"] for item in response.json()] == [course.id]


async def test_filter_schedules_by_teacher_id(client, db_session):
    teacher = await create_teacher(db_session)
    other_teacher = await create_teacher(db_session)
    await create_schedule(db_session, teacher=teacher)
    await create_schedule(db_session, teacher=other_teacher)

    response = await client.get("/schedules/", params={"teacher_id": teacher.id})

    assert response.status_code == 200
    assert [item["teacher_id"] for item in response.json()] == [teacher.id]


async def test_filter_schedules_not_found(client):
    assert (await client.get("/schedules/", params={"group": "Nope"})).status_code == 404


async def test_filter_schedules_by_room_zero(client, db_session):
    await create_schedule(db_session, room=0)
    await create_schedule(db_session, room=202)

    response = await client.get("/schedules/", params={"room": 0})

    assert response.status_code == 200
    assert [item["room"] for item in response.json()] == [0]


async def test_update_schedule_partial(client, db_session):
    schedule = await create_schedule(db_session, room=101)

    response = await client.patch(f"/schedules/{schedule.id}", json={"room": 202})

    assert response.status_code == 200
    assert response.json()["room"] == 202


async def test_update_schedule_not_found(client):
    response = await client.patch("/schedules/999", json={"room": 202})

    assert response.status_code == 404


async def test_delete_schedule(client, db_session):
    schedule = await create_schedule(db_session)

    response = await client.delete(f"/schedules/{schedule.id}")

    assert response.status_code == 204

    remaining = await client.get("/schedules/")
    assert schedule.id not in [item["id"] for item in remaining.json()]
