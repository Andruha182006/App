from typing import Sequence

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import get_current_user
from core.database import get_db
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
    db: AsyncSession = Depends(get_db),
):
    if filters.group:
        return await schedule_service.get_by_group(
            db, group=filters.group, skip=skip, limit=limit
        )

    if filters.room is not None:
        return await schedule_service.get_by_room(
            db, room=filters.room, skip=skip, limit=limit
        )

    if filters.teacher_id is not None:
        return await schedule_service.get_by_teacher_id(
            db, teacher_id=filters.teacher_id, skip=skip, limit=limit
        )

    if filters.course_id is not None:
        return await schedule_service.get_by_course_id(
            db, course_id=filters.course_id, skip=skip, limit=limit
        )

    return await schedule_service.get_all(db, skip=skip, limit=limit)


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def read_schedule_by_id(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await schedule_service.get_by_id(db, id=schedule_id)


@router.patch("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: int,
    data: ScheduleUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await schedule_service.update(db, id=schedule_id, data=data)


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
):
    await schedule_service.delete(db, id=schedule_id)
