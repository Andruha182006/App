from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.courses import Course
from repository import course_rep
from schemas.courses import CoursesCreate, CoursesUpdate
from services.base import ServiceBase


# Дженеріки: Course (Model), CoursesCreate (CreateSchema), CoursesUpdate (UpdateSchema)
class CourseService(ServiceBase[Course, CoursesCreate, CoursesUpdate]):
    def __init__(self):
        super().__init__(repository=course_rep)

    async def get_by_title(
        self, db: AsyncSession, title: str, skip: int = 0, limit: int = 100
    ) -> Sequence[Course]:
        courses = await self.repository.get_by_title(
            db, title=title, skip=skip, limit=limit
        )
        if not courses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repository.model.__name__} with title '{title}' not found",
            )
        return courses

    async def get_by_credits(
        self, db: AsyncSession, credits: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Course]:
        courses = await self.repository.get_by_credits(
            db, credits=credits, skip=skip, limit=limit
        )
        if not courses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repository.model.__name__} with {credits} credits not found",
            )
        return courses

    async def get_course_credits(self, db: AsyncSession, course_id: int) -> int:
        course = await self.get_by_id(db, id=course_id)
        return course.credits

    async def get_by_teacher_id(
        self, db: AsyncSession, teacher_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Course]:
        courses = await self.repository.get_by_teacher_id(
            db, teacher_id=teacher_id, skip=skip, limit=limit
        )
        if not courses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repository.model.__name__} for teacher with id {teacher_id} not found",
            )
        return courses



course_service = CourseService()