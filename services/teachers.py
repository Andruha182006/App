from typing import Sequence
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.enums import UserRole
from models import Teacher
from repository.teachers import teacher_rep
from repository.users import user_repository
from schemas.teachers import TeacherCreate, TeacherUpdate
from services.base import ServiceBase


class TeacherService(ServiceBase[Teacher, TeacherCreate, TeacherUpdate]):
    def __init__(self):
        super().__init__(repository=teacher_rep)

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
        if user.role != UserRole.teacher:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User must have teacher role",
            )

        linked_teacher = await self.repository.get_by_user_id(db, user_id=user_id)
        if linked_teacher is not None and linked_teacher.id != profile_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already linked to another teacher",
            )

    async def create(self, db: AsyncSession, data: TeacherCreate) -> Teacher:
        await self._validate_user_link(db, data.user_id)
        return await super().create(db, data)

    async def update(
        self,
        db: AsyncSession,
        id: int,
        data: TeacherUpdate,
    ) -> Teacher:
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
