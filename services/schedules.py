from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from models import Schedule
from repository.schedules import schedule_rep
from schemas.schedules import ScheduleCreate, ScheduleUpdate
from services.base import ServiceBase


class ScheduleService(ServiceBase[Schedule, ScheduleCreate, ScheduleUpdate]):
    def __init__(self):
        super().__init__(repository=schedule_rep)

    async def get_by_group(
        self,
        db: AsyncSession,
        group: str,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Schedule]:
        return await self.repository.get_by_group(
            db, group=group, skip=skip, limit=limit
        )

    async def get_by_room(
        self,
        db: AsyncSession,
        room: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Schedule]:
        return await self.repository.get_by_room(
            db, room=room, skip=skip, limit=limit
        )

    async def get_by_course_id(
        self,
        db: AsyncSession,
        course_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Schedule]:
        return await self.repository.get_by_course_id(
            db, course_id=course_id, skip=skip, limit=limit
        )

    async def get_by_teacher_id(
        self,
        db: AsyncSession,
        teacher_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Schedule]:
        return await self.repository.get_by_teacher_id(
            db, teacher_id=teacher_id, skip=skip, limit=limit
        )


schedule_service = ScheduleService()
