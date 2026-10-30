from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from models.courses import Course
from repository import course_rep
from schemas.courses import CoursesCreate, CoursesUpdate
from services.base import ServiceBase


class CourseService(ServiceBase[Course, CoursesCreate, CoursesUpdate]):
    def __init__(self):
        super().__init__(repository=course_rep)

    async def get_by_title(
        self,
        db: AsyncSession,
        title: str,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Course]:
        return await self.repository.get_by_title(
            db, title=title, skip=skip, limit=limit
        )

    async def get_by_credits(
        self,
        db: AsyncSession,
        credits: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Course]:
        return await self.repository.get_by_credits(
            db, credits=credits, skip=skip, limit=limit
        )

    async def get_by_teacher_id(
        self,
        db: AsyncSession,
        teacher_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Course]:
        return await self.repository.get_by_teacher_id(
            db, teacher_id=teacher_id, skip=skip, limit=limit
        )


course_service = CourseService()
