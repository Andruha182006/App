"""Фабрики тестових об'єктів.

Кожен хелпер створює запис у тестовій БД і повертає ORM-об'єкт.
Email генерується унікальним, щоб не конфліктувати з unique-обмеженнями.
"""

from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_password_hash
from models.courses import Course
from models.schedules import Schedule
from models.students import Student
from models.tasks import Task
from models.teachers import Teacher
from models.users import User


def _unique_email(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12]}@example.com"


async def create_student(
    db: AsyncSession,
    *,
    name: str = "Alice",
    age: int = 20,
    email: str | None = None,
) -> Student:
    student = Student(name=name, age=age, email=email or _unique_email("student"))
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


async def create_teacher(
    db: AsyncSession,
    *,
    name: str = "Bob",
    department: str = "Math",
    email: str | None = None,
) -> Teacher:
    teacher = Teacher(name=name, department=department, email=email or _unique_email("teacher"))
    db.add(teacher)
    await db.commit()
    await db.refresh(teacher)
    return teacher


async def create_course(
    db: AsyncSession,
    *,
    title: str = "Algebra",
    credits: int = 5,
    teacher: Teacher | None = None,
) -> Course:
    teacher = teacher or await create_teacher(db)
    course = Course(title=title, credits=credits, teacher_id=teacher.id)
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course


async def create_task(
    db: AsyncSession,
    *,
    title: str = "Homework",
    student: Student | None = None,
    teacher: Teacher | None = None,
) -> Task:
    student = student or await create_student(db)
    teacher = teacher or await create_teacher(db)
    task = Task(title=title, student_id=student.id, teacher_id=teacher.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def create_schedule(
    db: AsyncSession,
    *,
    group: str = "KN-21",
    room: int = 101,
    course: Course | None = None,
    teacher: Teacher | None = None,
) -> Schedule:
    teacher = teacher or await create_teacher(db)
    course = course or await create_course(db, teacher=teacher)
    schedule = Schedule(
        group=group,
        room=room,
        course_id=course.id,
        teacher_id=teacher.id,
    )
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    return schedule


async def create_user(
    db: AsyncSession,
    *,
    email: str | None = None,
    name: str = "Test User",
    password: str = "secret123",
    is_active: bool = True,
    is_superuser: bool = False,
) -> User:
    user = User(
        email=email or _unique_email("user"),
        name=name,
        hashed_password=get_password_hash(password),
        is_active=is_active,
        is_superuser=is_superuser,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
