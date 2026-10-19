
from models import Schedule
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from services.base import ServiceBase
from repository.schedules import schedule_rep
from schemas.schedules import ScheduleCreate,ScheduleUpdate

class ScheduleService(ServiceBase[Schedule,ScheduleCreate,ScheduleUpdate]):
    def __init__(self):
        super().__init__(repository=schedule_rep)

    async def get_by_group(
            self, db: AsyncSession, group: str, skip: int = 0, limit: int = 100) -> Sequence[Schedule]:
        schedules = await self.repository.get_by_group(
            db, group=group, skip=skip, limit=limit
        )
        if not schedules:
            raise HTTPException(status_code=404,detail=f"Schedule for group '{group}' not found",)
        return schedules

    async def get_by_room(self,db:AsyncSession,room:int,skip:int = 0, limit:int =100) ->Sequence[Schedule]:
        schedules = await self.repository.get_by_room(db,room=room,skip=skip,limit=limit)
        if not schedules:
            raise HTTPException(status_code=404,detail=f'Schedule for room {room} not found')
        return schedules

    async def get_by_course_id(self,db:AsyncSession,course_id: int, skip: int = 0, limit: int = 100) -> Sequence[Schedule]:
        schedules = await self.repository.get_by_course_id(db,course_id=course_id,skip=skip,limit=limit)
        if not schedules:
            raise HTTPException(status_code=404,detail=f'Schedule for course {course_id} not found')
        return schedules

    async def get_by_teacher_id(self,db:AsyncSession,teacher_id: int, skip: int = 0, limit: int = 100) -> Sequence[Schedule]:
        schedules = await self.repository.get_by_teacher_id(db,course_id=teacher_id,skip=skip,limit=limit)
        if not schedules:
            raise HTTPException(status_code=404,detail=f'Schedule for course {teacher_id} not found')
        return schedules

schedule_service = ScheduleService()
