from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from repository.base import CRUDBase
from models.tasks import Task
from typing import Sequence

class TaskRepository(CRUDBase[Task]):
    def __init__(self):
        super().__init__(Task)

    async def get_by_title(self,db:AsyncSession,title:str,skip: int = 0,limit:int = 100) -> Sequence[Task]:
        query = select(self.model).where(self.model.title == title).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_student_id(self,db:AsyncSession,student_id:int,skip: int = 0,limit:int = 100) -> Sequence[Task]:
        query = select(self.model).where(self.model.student_id == student_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_teacher_id(self,db:AsyncSession,teacher_id:int,skip: int = 0,limit:int = 100) -> Sequence[Task]:
        query = select(self.model).where(self.model.teacher_id == teacher_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

task_rep = TaskRepository()



