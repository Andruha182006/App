from models import Teacher
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from schemas.teachers import TeacherCreate, TeacherUpdate
from services.base import ServiceBase
from repository.teachers import teacher_rep

class TeacherService(ServiceBase[Teacher,TeacherCreate,TeacherUpdate]):
    def __init__(self):
        super().__init__(repository = teacher_rep)

    async def get_by_name(self,db:AsyncSession,name:str,skip:int = 0,limit:int = 100) ->Sequence[Teacher]:
        teachers = await self.repository.get_by_name(db,name = name,skip = skip,limit = limit)
        if not teachers:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with name {name} not found')
        return teachers

    async def get_by_department(self,db:AsyncSession,department:str,skip:int = 0,limit:int = 100) ->Sequence[Teacher]:
        teachers = await self.repository.get_by_department(db, department=department, skip=skip, limit=limit)
        if not teachers:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with department {department} not found')
        return teachers

    async def get_by_email(self,db:AsyncSession,email:str) -> Teacher:
        teacher = await self.repository.get_by_email(db,email=email)
        if not teacher:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__}with email {email} not found')
        return teacher

teacher_service = TeacherService()