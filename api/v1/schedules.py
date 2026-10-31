from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import (
    get_current_user,
    load_student_profile,
    load_teacher_profile,
    require_roles,
)
from core.database import get_db
from core.enums import UserRole
from models.users import User
from schemas.schedules import (
    ScheduleCreate,
    ScheduleFilter,
    ScheduleResponse,
    ScheduleUpdate,
)
from services.schedules import schedule_service

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/",
    response_model=ScheduleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def create_schedule(
    data: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
):
    return await schedule_service.create(db, data=data)


@router.get("/", response_model=Sequence[ScheduleResponse])
async def get_schedule(
    filters: ScheduleFilter = Depends(),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    group = filters.group
    teacher_id = filters.teacher_id

    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if teacher_id is not None and teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can view only your own schedule",
            )
        teacher_id = teacher.id
    elif current_user.role == UserRole.student:
        student = await load_student_profile(db, current_user)
        if student.group is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student group is not set",
            )
        if group is not None and group != student.group:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can view only your own group schedule",
            )
        group = student.group

    return await schedule_service.get_filtered(
        db,
        group=group,
        room=filters.room,
        teacher_id=teacher_id,
        course_id=filters.course_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def read_schedule_by_id(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    schedule = await schedule_service.get_by_id(db, id=schedule_id)

    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if schedule.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can view only your own schedule",
            )
    elif current_user.role == UserRole.student:
        student = await load_student_profile(db, current_user)
        if student.group is None or schedule.group != student.group:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can view only your own group schedule",
            )

    return schedule


@router.patch(
    "/{schedule_id}",
    response_model=ScheduleResponse,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def update_schedule(
    schedule_id: int,
    data: ScheduleUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await schedule_service.update(db, id=schedule_id, data=data)


@router.delete(
    "/{schedule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def delete_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
):
    await schedule_service.delete(db, id=schedule_id)
