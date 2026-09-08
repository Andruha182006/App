from sqlalchemy import select
from sqlalchemy.orm import Session
from repository.base import CRUDBase
from models.schedules import Schedule

class ScheduleRepository(CRUDBase[Schedule]):
    def __init__(self):
        super().__init__(Schedule)

    def get_by_group(self,db:Session,group:str,skip: int = 0,limit:int = 100) -> list[Schedule]:
        query = select(self.model).where(self.model.group == group).offset(skip).limit(limit)
        return list(db.scalars(query).all())

    def get_by_room(self,db:Session,room:int,skip: int = 0,limit:int = 100) -> list[Schedule]:
        query = select(self.model).where(self.model.room == room ).offset(skip).limit(limit)
        return list(db.scalars(query).all())

    def get_by_course_id(self, db: Session, course_id: int, skip: int = 0, limit: int = 100) -> list[Schedule]:
        query = select(self.model).where(self.model.course_id == course_id).offset(skip).limit(limit)
        return list(db.scalars(query).all())

    def get_by_teacher_id(self, db: Session, teacher_id: int, skip: int = 0, limit: int = 100) -> list[Schedule]:
        query = select(self.model).where(self.model.teacher_id == teacher_id).offset(skip).limit(limit)
        return list(db.scalars(query).all())

schedule_rep = ScheduleRepository()



