from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from models import Task
from repository.tasks import task_rep
from schemas.tasks import TaskCreate, TaskUpdate
from services.base import ServiceBase


class TaskService(ServiceBase[Task, TaskCreate, TaskUpdate]):
    def __init__(self):
        super().__init__(repository=task_rep)

    async def get_by_title(
        self,
        db: AsyncSession,
        title: str,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Task]:
        return await self.repository.get_by_title(
            db, title=title, skip=skip, limit=limit
        )

    async def get_by_student_id(
        self,
        db: AsyncSession,
        student_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Task]:
        return await self.repository.get_by_student_id(
            db, student_id=student_id, skip=skip, limit=limit
        )

    async def get_by_teacher_id(
        self,
        db: AsyncSession,
        teacher_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Task]:
        return await self.repository.get_by_teacher_id(
            db, teacher_id=teacher_id, skip=skip, limit=limit
        )


task_service = TaskService()
