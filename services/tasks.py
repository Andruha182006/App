from models import Task
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from services.base import ServiceBase
from repository.tasks import task_rep
from schemas.tasks import TaskCreate,TaskUpdate

class TaskService(ServiceBase[Task,TaskUpdate,TaskCreate]):
    def __init__(self):
        super().__init__(repository=task_rep)

    async def get_by_title(self,db:AsyncSession,title:str,skip:int = 0,limit:int =100) -> Sequence[Task]:
        tasks = await self.repository.get_by_title(db,title=title,skip=skip,limit=limit)
        if not tasks:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with title{title} not found')
        return tasks

    async def get_by_student_id(self,db:AsyncSession,student_id:int,skip:int =0,limit:int =100) -> Sequence[Task]:
        tasks = await self.repository.get_by_student_id(db,student_id=student_id,skip=skip,limit=limit)
        if not tasks:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with student{student_id} not found')
        return tasks

    async def get_by_teacher_id(self,db:AsyncSession,teacher_id:int,skip:int =0,limit:int =100) -> Sequence[Task]:
        tasks = await self.repository.get_by_teacher_id(db,teacher_id=teacher_id,skip=skip,limit=limit)
        if not tasks:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with teacher{teacher_id} not found')
        return tasks

task_service = TaskService()