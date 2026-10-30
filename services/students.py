from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from models import Student
from repository.students import student_rep
from schemas.students import StudentCreate, StudentUpdate
from services.base import ServiceBase


class StudentService(ServiceBase[Student, StudentCreate, StudentUpdate]):
    def __init__(self):
        super().__init__(repository=student_rep)

    async def get_by_name(
        self,
        db: AsyncSession,
        name: str,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Student]:
        return await self.repository.get_by_name(
            db, name=name, skip=skip, limit=limit
        )

    async def get_by_age(
        self,
        db: AsyncSession,
        age: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Student]:
        return await self.repository.get_by_age(
            db, age=age, skip=skip, limit=limit
        )

    async def get_by_email(
        self,
        db: AsyncSession,
        email: str,
    ) -> Student | None:
        return await self.repository.get_by_email(db, email=email)


student_service = StudentService()
