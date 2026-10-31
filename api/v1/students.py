from typing import Sequence

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import (
    get_current_student,
    get_current_user,
    require_roles,
)
from core.database import get_db
from core.enums import UserRole
from models.students import Student
from schemas.students import (
    StudentCreate,
    StudentFilter,
    StudentResponse,
    StudentUpdate,
)
from services.students import student_service

router = APIRouter(
    prefix="/students",
    tags=["Students"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/me", response_model=StudentResponse)
async def read_my_student_profile(
    current_student: Student = Depends(get_current_student),
):
    return current_student


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def get_student_by_id(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await student_service.get_by_id(db, id=student_id)


@router.get(
    "/",
    response_model=Sequence[StudentResponse],
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def read_students(
    filter: StudentFilter = Depends(),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    if filter.name:
        return await student_service.get_by_name(
            db, name=filter.name, skip=skip, limit=limit
        )

    if filter.age is not None:
        return await student_service.get_by_age(
            db, age=filter.age, skip=skip, limit=limit
        )

    if filter.email:
        student = await student_service.get_by_email(
            db, email=str(filter.email)
        )
        return [student] if student else []

    return await student_service.get_all(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def create_student(
    data: StudentCreate,
    db: AsyncSession = Depends(get_db),
):
    return await student_service.create(db, data=data)


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def update_student(
    student_id: int,
    data: StudentUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await student_service.update(db, id=student_id, data=data)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    await student_service.delete(db, id=student_id)
