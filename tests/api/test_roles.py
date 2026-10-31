"""Тести рольового доступу та перевірки власності."""

from models.students import Student
from models.teachers import Teacher
from tests.factories import (
    create_course,
    create_schedule,
    create_student,
    create_task,
    create_teacher,
)


async def _teacher_id(client) -> int:
    response = await client.get("/teachers/me")
    assert response.status_code == 200
    return response.json()["id"]


async def _student_id(client) -> int:
    response = await client.get("/students/me")
    assert response.status_code == 200
    return response.json()["id"]


async def test_student_cannot_write_anything(student_client):
    assert (
        await student_client.post(
            "/students/",
            json={
                "name": "Alice",
                "age": 20,
                "email": "alice@example.com",
            },
        )
    ).status_code == 403
    assert (
        await student_client.post(
            "/teachers/",
            json={
                "name": "Bob",
                "email": "bob@example.com",
                "department": "Math",
            },
        )
    ).status_code == 403
    assert (
        await student_client.post(
            "/courses/",
            json={"title": "Algebra", "credits": 5, "teacher_id": 1},
        )
    ).status_code == 403
    assert (
        await student_client.post(
            "/tasks/",
            json={"title": "Homework", "student_id": 1, "teacher_id": 1},
        )
    ).status_code == 403
    assert (
        await student_client.post(
            "/schedules/",
            json={
                "course_id": 1,
                "teacher_id": 1,
                "group": "KN-21",
                "room": 101,
            },
        )
    ).status_code == 403


async def test_teacher_cannot_manage_schedules_or_profiles(teacher_client):
    assert (
        await teacher_client.post(
            "/students/",
            json={
                "name": "Alice",
                "age": 20,
                "email": "alice@example.com",
            },
        )
    ).status_code == 403
    assert (
        await teacher_client.post(
            "/teachers/",
            json={
                "name": "Bob",
                "email": "bob@example.com",
                "department": "Math",
            },
        )
    ).status_code == 403
    assert (
        await teacher_client.post(
            "/schedules/",
            json={
                "course_id": 1,
                "teacher_id": 1,
                "group": "KN-21",
                "room": 101,
            },
        )
    ).status_code == 403
    assert (
        await teacher_client.get("/admin/users")
    ).status_code == 403


async def test_teacher_can_manage_only_own_courses(teacher_client, db_session):
    teacher_id = await _teacher_id(teacher_client)
    other_teacher = await create_teacher(db_session)
    other_teacher_id = other_teacher.id
    other_course = await create_course(
        db_session,
        title="Other course",
        teacher=other_teacher,
    )
    other_course_id = other_course.id

    created = await teacher_client.post(
        "/courses/",
        json={
            "title": "My course",
            "credits": 4,
            "teacher_id": teacher_id,
        },
    )
    assert created.status_code == 201
    own_course_id = created.json()["id"]

    forbidden_create = await teacher_client.post(
        "/courses/",
        json={
            "title": "Not mine",
            "credits": 3,
            "teacher_id": other_teacher_id,
        },
    )
    assert forbidden_create.status_code == 403

    listing = await teacher_client.get("/courses/")
    assert listing.status_code == 200
    assert {item["id"] for item in listing.json()} == {own_course_id}

    assert (
        await teacher_client.patch(
            f"/courses/{other_course_id}",
            json={"title": "Changed"},
        )
    ).status_code == 403
    assert (
        await teacher_client.delete(f"/courses/{other_course_id}")
    ).status_code == 403

    updated = await teacher_client.patch(
        f"/courses/{own_course_id}",
        json={"title": "Updated course"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Updated course"


async def test_teacher_can_manage_only_own_tasks(teacher_client, db_session):
    teacher_id = await _teacher_id(teacher_client)
    teacher = await db_session.get(Teacher, teacher_id)
    student = await create_student(db_session)
    student_id = student.id
    own_task = await create_task(
        db_session,
        title="My task",
        student=student,
        teacher=teacher,
    )
    own_task_id = own_task.id
    other_task = await create_task(db_session, title="Other task")
    other_task_id = other_task.id
    other_task_teacher_id = other_task.teacher_id

    listing = await teacher_client.get("/tasks/")
    assert listing.status_code == 200
    assert {item["id"] for item in listing.json()} == {own_task_id}

    assert (
        await teacher_client.get(f"/tasks/{other_task_id}")
    ).status_code == 403
    assert (
        await teacher_client.patch(
            f"/tasks/{other_task_id}",
            json={"title": "Changed"},
        )
    ).status_code == 403
    assert (
        await teacher_client.delete(f"/tasks/{other_task_id}")
    ).status_code == 403

    forbidden_create = await teacher_client.post(
        "/tasks/",
        json={
            "title": "Not mine",
            "student_id": student_id,
            "teacher_id": other_task_teacher_id,
        },
    )
    assert forbidden_create.status_code == 403

    created = await teacher_client.post(
        "/tasks/",
        json={
            "title": "Created by teacher",
            "student_id": student_id,
            "teacher_id": teacher_id,
        },
    )
    assert created.status_code == 201

    updated = await teacher_client.patch(
        f"/tasks/{own_task_id}",
        json={"title": "Updated task"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Updated task"


async def test_student_can_read_only_own_tasks(student_client, db_session):
    student_id = await _student_id(student_client)
    student = await db_session.get(Student, student_id)
    own_task = await create_task(db_session, student=student)
    own_task_id = own_task.id
    other_task = await create_task(db_session)
    other_task_id = other_task.id
    other_task_student_id = other_task.student_id

    listing = await student_client.get("/tasks/")
    assert listing.status_code == 200
    assert {item["id"] for item in listing.json()} == {own_task_id}

    assert (
        await student_client.get(f"/tasks/{own_task_id}")
    ).status_code == 200
    assert (
        await student_client.get(f"/tasks/{other_task_id}")
    ).status_code == 403
    assert (
        await student_client.get(
            "/tasks/",
            params={"student_id": other_task_student_id},
        )
    ).status_code == 403


async def test_student_can_read_only_own_group_schedule(
    student_client,
    db_session,
):
    own_schedule = await create_schedule(db_session, group="KN-21")
    own_schedule_id = own_schedule.id
    other_schedule = await create_schedule(db_session, group="KN-22")
    other_schedule_id = other_schedule.id

    listing = await student_client.get("/schedules/")
    assert listing.status_code == 200
    assert {item["id"] for item in listing.json()} == {own_schedule_id}

    assert (
        await student_client.get(f"/schedules/{other_schedule_id}")
    ).status_code == 403
    assert (
        await student_client.get(
            "/schedules/",
            params={"group": "KN-22"},
        )
    ).status_code == 403
    assert (
        await student_client.get(
            "/schedules/",
            params={"group": "KN-21"},
        )
    ).status_code == 200


async def test_teacher_can_read_only_own_schedule(teacher_client, db_session):
    teacher_id = await _teacher_id(teacher_client)
    teacher = await db_session.get(Teacher, teacher_id)
    own_schedule = await create_schedule(
        db_session,
        group="KN-21",
        teacher=teacher,
    )
    own_schedule_id = own_schedule.id
    other_schedule = await create_schedule(db_session, group="KN-22")
    other_schedule_id = other_schedule.id
    other_schedule_teacher_id = other_schedule.teacher_id

    listing = await teacher_client.get("/schedules/")
    assert listing.status_code == 200
    assert {item["id"] for item in listing.json()} == {own_schedule_id}

    assert (
        await teacher_client.get(f"/schedules/{other_schedule_id}")
    ).status_code == 403
    assert (
        await teacher_client.get(
            "/schedules/",
            params={"teacher_id": other_schedule_teacher_id},
        )
    ).status_code == 403


async def test_teacher_cannot_list_students(teacher_client):
    assert (await teacher_client.get("/students/")).status_code == 403


async def test_student_cannot_list_teachers(student_client):
    assert (await student_client.get("/teachers/")).status_code == 403
