from models import Student
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from schemas.students import StudentCreate,StudentUpdate
from services.base import ServiceBase
from repository.students import student_rep

class StudentService(ServiceBase[Student,StudentUpdate,StudentCreate]):
    def __init__(self):
        super().__init__(repository=student_rep)

    async def get_by_name(self,db:AsyncSession,name:str,skip:int = 0,limit:int = 100) ->Sequence[Student]:
        students = await self.repository.get_by_name(db,name = name,skip = skip,limit = limit)
        if not students:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with name {name} not found')
        return students

    async def get_by_age(self,db:AsyncSession,age:int,skip:int = 0,limit:int = 100) ->Sequence[Student]:
        students = await self.repository.get_by_age(db, age=age, skip=skip, limit=limit)
        if not students:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with department {age} not found')
        return students

    async def get_by_email(self,db:AsyncSession,email:str) -> Student:
        students = await self.repository.get_by_email(db,email=email)
        if not students:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__}with email {email} not found')
        return students

student_service = StudentService()