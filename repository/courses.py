from sqlalchemy import select
from sqlalchemy.orm import Session
from repository.base import CRUDBase
from models.courses import Course

class CourseRepository(CRUDBase[Course]):
    def __init__(self):
        super().__init__(Course)

    def get_by_name(self,db:Session,name:str, skip: int = 0,limit:int = 100) -> list[Course]:
        query = select(self.model).where(self.model.name == name).offset(skip).limit(limit)
        return list(db.scalars(query).all())

    def get_by_credits(self, db: Session, credits: int, skip: int = 0, limit: int = 100) -> list[Course]:
        query = select(self.model).where(self.model.credits == credits).offset(skip).limit(limit)
        return list(db.scalars(query).all())

    def get_by_teacher_id(self, db: Session, teacher_id: int, skip: int = 0, limit: int = 100) -> list[Course]:
        query = select(self.model).where(self.model.teacher_id == teacher_id).offset(skip).limit(limit)
        return list(db.scalars(query).all())

course_rep = CourseRepository()



