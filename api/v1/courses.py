from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import (
    get_current_user,
    load_teacher_profile,
    require_roles,
)
from core.database import get_db
from core.enums import UserRole
from models.users import User
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
    current_user: User = Depends(
        require_roles(UserRole.admin, UserRole.teacher)
    ),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if data.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can create courses only for yourself",
            )
    return await course_service.create(db, data=data)


@router.get("/{course_id}", response_model=CourseResponse)
async def read_course_by_id(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    course = await course_service.get_by_id(db, id=course_id)
    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if course.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can view only your own courses",
            )
    return course


@router.get("/", response_model=Sequence[CourseResponse])
async def get_courses(
    filters: CourseFilter = Depends(),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    teacher_id = filters.teacher_id

    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if teacher_id is not None and teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can view only your own courses",
            )
        teacher_id = teacher.id

    return await course_service.get_filtered(
        db,
        teacher_id=teacher_id,
        title=filters.title,
        credits=filters.credits,
        skip=skip,
        limit=limit,
    )


@router.patch("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    data: CoursesUpdate,
    current_user: User = Depends(
        require_roles(UserRole.admin, UserRole.teacher)
    ),
    db: AsyncSession = Depends(get_db),
):
    course = await course_service.get_by_id(db, id=course_id)

    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if course.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can update only your own courses",
            )
        if data.teacher_id is not None and data.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot reassign a course to another teacher",
            )

    return await course_service.update(db, id=course_id, data=data)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    current_user: User = Depends(
        require_roles(UserRole.admin, UserRole.teacher)
    ),
    db: AsyncSession = Depends(get_db),
):
    course = await course_service.get_by_id(db, id=course_id)

    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if course.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can delete only your own courses",
            )

    await course_service.delete(db, id=course_id)
