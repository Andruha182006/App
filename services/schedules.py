from models import Schedule
from fastapi import HTTPException
from sqlalchemy.orm import Session
from services.base import ServiceBase
from repository.schedules import schedule_rep
from schemas.schedules import ScheduleCreate,ScheduleUpdate

class ScheduleService(ServiceBase[Schedule,ScheduleUpdate,ScheduleCreate]):
    def __init__(self):
        super().__init__(repository=schedule_rep)

    def get_by_group(
            self, db: Session, group: str, skip: int = 0, limit: int = 100
    ) -> list[Schedule]:
        schedules = self.repository.get_by_group(
            db, group=group, skip=skip, limit=limit
        )
        if not schedules:
            raise HTTPException(
                status_code=404,
                detail=f"Schedule for group '{group}' not found",
            )
        return schedules

schedule_service = ScheduleService()