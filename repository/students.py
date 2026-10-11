from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from repository.base import CRUDBase
from models.students import Student
from typing import Sequence

class StudentRepository(CRUDBase[Student]):
    def __init__(self):
        super().__init__(Student)

    async def get_by_email(self,db: AsyncSession,email:str) -> Student|None:
        query = select(self.model).where(self.model.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_name(self,db:AsyncSession,name:str,skip: int = 0,limit:int = 100) -> Sequence[Student]:
        query = select(self.model).where(self.model.name == name).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_age(self,db:AsyncSession,age:int,skip: int = 0,limit:int = 100) -> Sequence[Student]:
        query = select(self.model).where(self.model.age == age ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

student_rep = StudentRepository()



