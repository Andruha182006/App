"""Юніт-тести для Pydantic-схем.

Перевіряємо валідацію вхідних даних і серіалізацію відповідей.
"""

import pytest
from pydantic import ValidationError

from schemas.courses import CoursesCreate, CoursesUpdate, CourseResponse
from schemas.schedules import ScheduleCreate, ScheduleUpdate
from schemas.students import StudentCreate, StudentResponse, StudentUpdate
from schemas.tasks import TaskCreate, TaskUpdate
from schemas.teachers import TeacherCreate, TeacherUpdate
from schemas.tokens import Token
from schemas.users import UserCreate, UserResponse


class TestUserSchemas:
    def test_user_create_valid(self):
        user = UserCreate(name="Alice", email="alice@example.com", password="password123")

        assert user.email == "alice@example.com"
        assert user.name == "Alice"

    def test_user_create_rejects_invalid_email(self):
        with pytest.raises(ValidationError):
            UserCreate(name="Alice", email="not-an-email", password="password123")

    def test_user_create_rejects_short_password(self):
        with pytest.raises(ValidationError):
            UserCreate(name="Alice", email="alice@example.com", password="short")

    def test_user_create_rejects_short_name(self):
        with pytest.raises(ValidationError):
            UserCreate(name="A", email="alice@example.com", password="password123")

    def test_user_response_has_no_password_field(self):
        response = UserResponse(
            id="12345678-1234-5678-1234-567812345678",
            name="Alice",
            email="alice@example.com",
            is_active=True,
        )

        assert "password" not in response.model_dump()
        assert response.model_dump()["is_active"] is True


class TestStudentSchemas:
    def test_student_create_requires_all_fields(self):
        with pytest.raises(ValidationError):
            StudentCreate(name="Alice", age=20)  # без email

    def test_student_create_rejects_zero_age(self):
        with pytest.raises(ValidationError):
            StudentCreate(name="Alice", age=0, email="alice@example.com")

    def test_student_create_rejects_long_name(self):
        with pytest.raises(ValidationError):
            StudentCreate(name="A" * 26, age=20, email="alice@example.com")

    def test_student_create_rejects_invalid_email(self):
        with pytest.raises(ValidationError):
            StudentCreate(name="Alice", age=20, email="not-an-email")

    def test_student_update_allows_empty_payload(self):
        update = StudentUpdate()

        assert update.model_dump(exclude_unset=True) == {}

    def test_student_update_excludes_unset_fields(self):
        update = StudentUpdate(age=21)

        assert update.model_dump(exclude_unset=True) == {"age": 21}

    def test_student_response_from_attributes(self):
        class OrmLike:
            id = 1
            name = "Alice"
            age = 20
            email = "alice@example.com"

        response = StudentResponse.model_validate(OrmLike())

        assert response.id == 1
        assert response.email == "alice@example.com"


class TestTeacherSchemas:
    def test_teacher_create_valid(self):
        teacher = TeacherCreate(name="Bob", email="bob@example.com", department="Math")

        assert teacher.department == "Math"

    def test_teacher_update_allows_partial_payload(self):
        update = TeacherUpdate(name="Bob")

        assert update.model_dump(exclude_unset=True) == {"name": "Bob"}

        full = TeacherUpdate(name="Bob", email="bob@example.com", department="Physics")
        assert full.department == "Physics"


class TestCourseSchemas:
    def test_course_create_requires_teacher_id(self):
        with pytest.raises(ValidationError):
            CoursesCreate(title="Algebra", credits=5)

    def test_course_create_rejects_negative_credits(self):
        with pytest.raises(ValidationError):
            CoursesCreate(title="Algebra", credits=-1, teacher_id=1)

    def test_course_update_allows_partial_payload(self):
        update = CoursesUpdate(credits=6)

        assert update.model_dump(exclude_unset=True) == {"credits": 6}

    def test_course_response_from_attributes(self):
        class OrmLike:
            id = 1
            title = "Algebra"
            credits = 5
            teacher_id = 2

        assert CourseResponse.model_validate(OrmLike()).teacher_id == 2


class TestTaskAndScheduleSchemas:
    def test_task_update_allows_empty_payload(self):
        assert TaskUpdate().model_dump(exclude_unset=True) == {}

    def test_task_create_requires_ids(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="Homework")

    def test_schedule_create_valid(self):
        schedule = ScheduleCreate(course_id=1, teacher_id=2, group="KN-21", room=101)

        assert schedule.room == 101

    def test_schedule_update_allows_partial_payload(self):
        assert ScheduleUpdate(room=202).model_dump(exclude_unset=True) == {"room": 202}

    def test_schedule_create_rejects_negative_room(self):
        with pytest.raises(ValidationError):
            ScheduleCreate(course_id=1, teacher_id=2, group="KN-21", room=-1)


def test_token_defaults_to_bearer():
    token = Token(access_token="jwt.token.value")

    assert token.token_type == "bearer"
