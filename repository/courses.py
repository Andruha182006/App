from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from repository.base import CRUDBase
from models.courses import Course
from typing import Sequence

class CourseRepository(CRUDBase[Course]):
    def __init__(self):
        super().__init__(Course)

    async def get_by_name(self,db:AsyncSession,name:str, skip: int = 0,limit:int = 100) -> Sequence[Course]:
        query = select(self.model).where(self.model.name == name).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_by_credits(self, db: AsyncSession, credits: int, skip: int = 0, limit: int = 100) -> Sequence[Course]:
        query = select(self.model).where(self.model.credits == credits).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_by_teacher_id(self, db: AsyncSession, teacher_id: int, skip: int = 0, limit: int = 100) -> Sequence[Course]:
        query = select(self.model).where(self.model.teacher_id == teacher_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

course_rep = CourseRepository()



