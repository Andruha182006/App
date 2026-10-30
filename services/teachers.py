from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from models import Teacher
from repository.teachers import teacher_rep
from schemas.teachers import TeacherCreate, TeacherUpdate
from services.base import ServiceBase


class TeacherService(ServiceBase[Teacher, TeacherCreate, TeacherUpdate]):
    def __init__(self):
        super().__init__(repository=teacher_rep)

    async def get_by_name(
        self,
        db: AsyncSession,
        name: str,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Teacher]:
        return await self.repository.get_by_name(
            db, name=name, skip=skip, limit=limit
        )

    async def get_by_department(
        self,
        db: AsyncSession,
        department: str,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Teacher]:
        return await self.repository.get_by_department(
            db, department=department, skip=skip, limit=limit
        )

    async def get_by_email(
        self,
        db: AsyncSession,
        email: str,
    ) -> Teacher | None:
        return await self.repository.get_by_email(db, email=email)


teacher_service = TeacherService()
