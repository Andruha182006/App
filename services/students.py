from typing import Sequence
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.enums import UserRole
from models import Student
from repository.students import student_rep
from repository.users import user_repository
from schemas.students import StudentCreate, StudentUpdate
from services.base import ServiceBase


class StudentService(ServiceBase[Student, StudentCreate, StudentUpdate]):
    def __init__(self):
        super().__init__(repository=student_rep)

    async def _validate_user_link(
        self,
        db: AsyncSession,
        user_id: UUID | None,
        profile_id: int | None = None,
    ) -> None:
        if user_id is None:
            return

        user = await user_repository.get_by_id(db, user_id=user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if user.role != UserRole.student:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User must have student role",
            )

        linked_student = await self.repository.get_by_user_id(db, user_id=user_id)
        if linked_student is not None and linked_student.id != profile_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already linked to another student",
            )

    async def create(self, db: AsyncSession, data: StudentCreate) -> Student:
        await self._validate_user_link(db, data.user_id)
        return await super().create(db, data)

    async def update(
        self,
        db: AsyncSession,
        id: int,
        data: StudentUpdate,
    ) -> Student:
        update_data = data.model_dump(exclude_unset=True)
        if "user_id" in update_data:
            await self._validate_user_link(
                db,
                update_data["user_id"],
                profile_id=id,
            )
        return await super().update(db, id=id, data=data)

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
