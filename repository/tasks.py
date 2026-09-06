from sqlalchemy import select
from sqlalchemy.orm import Session
from repository.base import CRUDBase
from models.tasks import Task

class TaskRepository(CRUDBase[Task]):
    def __init__(self):
        super().__init__(Task)

    def get_by_title(self,db:Session,title:str,skip: int = 0,limit:int = 100) -> list[Task]:
        query = select(self.model).where(self.model.title == title).offset(skip).limit(limit)
        return list(db.scalars(query).all())

    def get_by_student_id(self,db:Session,student_id:int,skip: int = 0,limit:int = 100) -> list[Task]:
        query = select(self.model).where(self.model.student_id == student_id).offset(skip).limit(limit)
        return list(db.scalars(query).all())

    def get_by_teacher_id(self,db:Session,teacher_id:int,skip: int = 0,limit:int = 100) -> list[Task]:
        query = select(self.model).where(self.model.teacher_id == teacher_id).offset(skip).limit(limit)
        return list(db.scalars(query).all())

task_rep = TaskRepository()



