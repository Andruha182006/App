
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


schedule_service = ScheduleService()
