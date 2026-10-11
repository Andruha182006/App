from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from repository.base import CRUDBase
from models.teachers import Teacher
from typing import Sequence

class TeacherRepository(CRUDBase[Teacher]):
    def __init__(self):
        super().__init__(Teacher)

    async def get_by_email(self,db: AsyncSession,email:str) -> Teacher|None:
        query = select(self.model).where(self.model.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_department(self,db:AsyncSession,department:str,skip: int = 0,limit:int = 100) -> Sequence[Teacher]:
        query = select(self.model).where(self.model.department == department).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_name(self,db:AsyncSession,name:str,skip: int = 0,limit:int = 100) -> Sequence[Teacher]:
        query = select(self.model).where(self.model.name == name).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

teacher_rep = TeacherRepository()



