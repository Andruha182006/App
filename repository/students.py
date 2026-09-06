from sqlalchemy import select
from sqlalchemy.orm import Session
from repository.base import CRUDBase
from models.students import Student

class StudentRepository(CRUDBase[Student]):
    def __init__(self):
        super().__init__(Student)

    def get_by_email(self,db: Session,email:str) -> Student|None:
        query = select(self.model).where(self.model.email == email)
        return db.scalar(query)

    def get_by_name(self,db:Session,name:str,skip: int = 0,limit:int = 100) -> list[Student]:
        query = select(self.model).where(self.model.name == name).offset(skip).limit(limit)
        return list(db.scalars(query).all())

    def get_by_age(self,db:Session,age:int,skip: int = 0,limit:int = 100) -> list[Student]:
        query = select(self.model).where(self.model.age == age ).offset(skip).limit(limit)
        return list(db.scalars(query).all())


student_rep = StudentRepository()



