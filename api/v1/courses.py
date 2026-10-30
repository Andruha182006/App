from typing import Sequence

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import get_current_user
from core.database import get_db
from schemas.courses import (
    CourseFilter,
    CourseResponse,
    CoursesCreate,
    CoursesUpdate,
)
from services.courses import course_service

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_course(
    data: CoursesCreate,
    db: AsyncSession = Depends(get_db),
):
    return await course_service.create(db, data=data)


@router.get("/{course_id}", response_model=CourseResponse)
async def read_course_by_id(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await course_service.get_by_id(db, id=course_id)


@router.get("/", response_model=Sequence[CourseResponse])
async def get_courses(
    filters: CourseFilter = Depends(),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    if filters.title:
        return await course_service.get_by_title(
            db, title=filters.title, skip=skip, limit=limit
        )

    if filters.teacher_id is not None:
        return await course_service.get_by_teacher_id(
            db, teacher_id=filters.teacher_id, skip=skip, limit=limit
        )

    if filters.credits is not None:
        return await course_service.get_by_credits(
            db, credits=filters.credits, skip=skip, limit=limit
        )

    return await course_service.get_all(db, skip=skip, limit=limit)


@router.patch("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    data: CoursesUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await course_service.update(db, id=course_id, data=data)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    await course_service.delete(db, id=course_id)
