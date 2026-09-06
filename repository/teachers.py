from sqlalchemy import select
from sqlalchemy.orm import Session
from repository.base import CRUDBase
from models.teachers import Teacher

class TeacherRepository(CRUDBase[Teacher]):
    def __init__(self):
        super().__init__(Teacher)

    def get_by_email(self,db: Session,email:str) -> Teacher|None:
        query = select(self.model).where(self.model.email == email)
        return db.scalar(query)

    def get_by_department(self,db:Session,department:str,skip: int = 0,limit:int = 100) -> list[Teacher]:
        query = select(self.model).where(self.model.department == department).offset(skip).limit(limit)
        return list(db.scalars(query).all())

    def get_by_name(self,db:Session,name:str,skip: int = 0,limit:int = 100) -> list[Teacher]:
        query = select(self.model).where(self.model.name == name).offset(skip).limit(limit)
        return list(db.scalars(query).all())

teacher_rep = TeacherRepository()



