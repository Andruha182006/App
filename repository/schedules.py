
from sqlalchemy import select
from repository.base import CRUDBase
from models.schedules import Schedule
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

class ScheduleRepository(CRUDBase[Schedule]):
    def __init__(self):
        super().__init__(Schedule)

    async def get_by_group(self,db:AsyncSession,group:str,skip: int = 0,limit:int = 100) -> Sequence[Schedule]:
        query = select(self.model).where(self.model.group == group).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_room(self,db:AsyncSession,room:int,skip: int = 0,limit:int = 100) -> Sequence[Schedule]:
        query = select(self.model).where(self.model.room == room ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_course_id(self, db: AsyncSession, course_id: int, skip: int = 0, limit: int = 100) -> Sequence[Schedule]:
        query = select(self.model).where(self.model.course_id == course_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_teacher_id(self, db: AsyncSession, teacher_id: int, skip: int = 0, limit: int = 100) -> Sequence[Schedule]:
        query = select(self.model).where(self.model.teacher_id == teacher_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_filtered(
        self,
        db: AsyncSession,
        *,
        group: str | None = None,
        room: int | None = None,
        teacher_id: int | None = None,
        course_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Schedule]:
        query = select(self.model)
        if group is not None:
            query = query.where(self.model.group == group)
        if room is not None:
            query = query.where(self.model.room == room)
        if teacher_id is not None:
            query = query.where(self.model.teacher_id == teacher_id)
        if course_id is not None:
            query = query.where(self.model.course_id == course_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

schedule_rep = ScheduleRepository()

