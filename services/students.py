from models import Student
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.students import StudentCreate,StudentUpdate
from services.base import ServiceBase
from repository.students import student_rep

class StudentService(ServiceBase[Student,StudentUpdate,StudentCreate]):
    def __init__(self):
        super().__init__(repository=student_rep)

    def get_by_name(self,db:Session,name:str,skip:int = 0,limit:int = 100) ->list[Student]:
        students = self.repository.get_by_name(db,name = name,skip = skip,limit = limit)
        if not students:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with name {name} not found')
        return students

    def get_by_age(self,db:Session,age:int,skip:int = 0,limit:int = 100) ->list[Student]:
        students = self.repository.get_by_age(db, age=age, skip=skip, limit=limit)
        if not students:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with department {age} not found')
        return students

    def get_by_email(self,db:Session,email:str) -> Student:
        students = self.repository.get_by_email(db,email=email)
        if not students:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__}with email {email} not found')
        return students

student_service = StudentService()