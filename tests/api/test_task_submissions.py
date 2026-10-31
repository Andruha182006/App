"""Тести здачі завдань студентом."""

from models.students import Student
from tests.factories import create_student, create_task


async def _student_profile_id(student_client) -> int:
    response = await student_client.get("/students/me")
    assert response.status_code == 200
    return response.json()["id"]


async def test_student_can_submit_own_task(student_client, db_session):
    student = await db_session.get(Student, await _student_profile_id(student_client))
    task = await create_task(db_session, title="Homework", student=student)

    response = await student_client.post(
        f"/tasks/{task.id}/submit",
        json={"answer": "My solution"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "submitted"
    assert body["answer"] == "My solution"
    assert body["submitted_at"] is not None


async def test_student_cannot_submit_another_students_task(
    student_client,
    db_session,
):
    other_student = await create_student(db_session, name="Other")
    task = await create_task(db_session, student=other_student)

    response = await student_client.post(
        f"/tasks/{task.id}/submit",
        json={"answer": "Wrong student"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You can submit only your own tasks"


async def test_teacher_cannot_submit_task(teacher_client, db_session):
    student = await create_student(db_session)
    task = await create_task(db_session, student=student)

    response = await teacher_client.post(
        f"/tasks/{task.id}/submit",
        json={"answer": "Teacher answer"},
    )

    assert response.status_code == 403


async def test_submission_rejects_empty_answer(student_client, db_session):
    student = await db_session.get(Student, await _student_profile_id(student_client))
    task = await create_task(db_session, student=student)

    response = await student_client.post(
        f"/tasks/{task.id}/submit",
        json={"answer": ""},
    )

    assert response.status_code == 422
