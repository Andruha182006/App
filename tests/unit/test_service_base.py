"""Юніт-тести для services.base.ServiceBase на фейковому репозиторії."""

from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from models.students import Student
from schemas.students import StudentCreate, StudentUpdate
from services.base import ServiceBase


def make_student(**overrides) -> Student:
    defaults = {"id": 1, "name": "Alice", "age": 20, "email": "alice@example.com"}
    defaults.update(overrides)
    return Student(**defaults)


def make_service() -> tuple[ServiceBase, AsyncMock]:
    repository = AsyncMock()
    repository.model = Student
    return ServiceBase(repository), repository


async def test_get_by_id_returns_object():
    service, repository = make_service()
    student = make_student()
    repository.get_by_id.return_value = student

    result = await service.get_by_id(object(), id=1)

    assert result is student
    repository.get_by_id.assert_awaited_once()


async def test_get_by_id_raises_404_when_missing():
    service, repository = make_service()
    repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await service.get_by_id(object(), id=999)

    assert exc_info.value.status_code == 404
    assert "Student" in exc_info.value.detail


async def test_get_all_passes_pagination():
    service, repository = make_service()
    repository.get_all.return_value = [make_student()]
    db = object()

    result = await service.get_all(db, skip=5, limit=10)

    assert len(result) == 1
    repository.get_all.assert_awaited_once_with(db, skip=5, limit=10)


async def test_create_dumps_schema_to_dict():
    service, repository = make_service()
    data = StudentCreate(name="Bob", age=22, email="bob@example.com")
    repository.create.return_value = make_student(name="Bob")

    await service.create(object(), data=data)

    repository.create.assert_awaited_once()
    _, kwargs = repository.create.call_args
    assert kwargs["obj_in_data"] == {
        "name": "Bob",
        "age": 22,
        "email": "bob@example.com",
    }


async def test_update_sends_only_provided_fields():
    service, repository = make_service()
    student = make_student()
    repository.get_by_id.return_value = student
    repository.update.return_value = student

    await service.update(object(), id=1, data=StudentUpdate(age=21))

    _, kwargs = repository.update.call_args
    assert kwargs == {"db_obj": student, "update_data": {"age": 21}}


async def test_update_missing_object_raises_404_before_update():
    service, repository = make_service()
    repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await service.update(object(), id=999, data=StudentUpdate(age=21))

    assert exc_info.value.status_code == 404
    repository.update.assert_not_awaited()


async def test_delete_existing_object():
    service, repository = make_service()
    repository.delete.return_value = True
    db = object()

    result = await service.delete(db, id=1)

    assert result is None
    repository.delete.assert_awaited_once_with(db, id=1)
    # Зайвий SELECT більше не виконується: репозиторій сам повертає False,
    # якщо об'єкта немає.
    repository.get_by_id.assert_not_awaited()


async def test_delete_missing_object_raises_404():
    service, repository = make_service()
    repository.delete.return_value = False

    with pytest.raises(HTTPException) as exc_info:
        await service.delete(object(), id=999)

    assert exc_info.value.status_code == 404
    assert "Student" in exc_info.value.detail
