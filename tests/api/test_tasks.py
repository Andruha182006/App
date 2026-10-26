"""Інтеграційні тести CRUD для /tasks."""

from tests.factories import create_student, create_task, create_teacher


async def test_create_task(client, db_session):
    student = await create_student(db_session)
    teacher = await create_teacher(db_session)

    response = await client.post(
        "/tasks/",
        json={"title": "Homework", "student_id": student.id, "teacher_id": teacher.id},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Homework"
    assert body["student_id"] == student.id
    assert body["teacher_id"] == teacher.id


async def test_create_task_validation_error(client):
    response = await client.post("/tasks/", json={"title": "Homework"})

    assert response.status_code == 422


async def test_get_task_by_id(client, db_session):
    task = await create_task(db_session, title="Homework")

    response = await client.get(f"/tasks/{task.id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Homework"


async def test_get_task_not_found(client):
    assert (await client.get("/tasks/999")).status_code == 404


async def test_list_tasks(client, db_session):
    await create_task(db_session, title="Homework")
    await create_task(db_session, title="Project")

    response = await client.get("/tasks/")

    assert response.status_code == 200
    assert {item["title"] for item in response.json()} == {"Homework", "Project"}


async def test_filter_tasks_by_title(client, db_session):
    await create_task(db_session, title="Homework")
    await create_task(db_session, title="Project")

    response = await client.get("/tasks/", params={"title": "Project"})

    assert response.status_code == 200
    assert [item["title"] for item in response.json()] == ["Project"]


async def test_filter_tasks_by_student_id(client, db_session):
    student = await create_student(db_session)
    other_student = await create_student(db_session)
    await create_task(db_session, title="Homework", student=student)
    await create_task(db_session, title="Project", student=other_student)

    response = await client.get("/tasks/", params={"student_id": student.id})

    assert response.status_code == 200
    assert [item["title"] for item in response.json()] == ["Homework"]


async def test_filter_tasks_by_teacher_id(client, db_session):
    teacher = await create_teacher(db_session)
    other_teacher = await create_teacher(db_session)
    await create_task(db_session, title="Homework", teacher=teacher)
    await create_task(db_session, title="Project", teacher=other_teacher)

    response = await client.get("/tasks/", params={"teacher_id": teacher.id})

    assert response.status_code == 200
    assert [item["title"] for item in response.json()] == ["Homework"]


async def test_filter_tasks_not_found(client):
    assert (await client.get("/tasks/", params={"title": "Nope"})).status_code == 404


async def test_update_task_partial(client, db_session):
    task = await create_task(db_session, title="Homework")

    response = await client.patch(f"/tasks/{task.id}", json={"title": "Project"})

    assert response.status_code == 200
    assert response.json()["title"] == "Project"


async def test_update_task_not_found(client):
    response = await client.patch("/tasks/999", json={"title": "Project"})

    assert response.status_code == 404


async def test_delete_task(client, db_session):
    task = await create_task(db_session)

    response = await client.delete(f"/tasks/{task.id}")

    assert response.status_code == 204
    assert (await client.get(f"/tasks/{task.id}")).status_code == 404
