from models import Schedule
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from services.base import ServiceBase
from repository.schedules import schedule_rep
from repository.courses import course_rep
from repository.teachers import teacher_rep
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

    def create(self, db: Session, data: ScheduleCreate):
        # 1. Перевіряємо існування курсу
        course = course_rep.get_by_id(db, id=data.course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with id {data.course_id} does not exist"
            )

        # 2. Перевіряємо існування викладача
        teacher = teacher_rep.get_by_id(db, id=data.teacher_id)
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Teacher with id {data.teacher_id} does not exist"
            )

        # 3. Якщо батьківські сутності існують — зберігаємо розклад
        return self.repository.create(db, obj_in_data=data.model_dump())

schedule_service = ScheduleService()