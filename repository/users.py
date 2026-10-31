from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.enums import UserRole
from models.users import User


class UserRepository:
    async def get_by_id(self, db: AsyncSession, user_id: UUID) -> Optional[User]:
        return await db.get(User, user_id)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[User]:
        result = await db.execute(
            select(User).order_by(User.email).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(
        self,
        db: AsyncSession,
        *,
        email: str,
        name: str,
        hashed_password: str,
        role: UserRole = UserRole.student,
        is_active: bool = True,
    ) -> User:
        db_user = User(
            email=email,
            name=name,
            hashed_password=hashed_password,
            is_active=is_active,
            role=role,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def update(
        self,
        db: AsyncSession,
        *,
        user: User,
        update_data: dict,
    ) -> User:
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


user_repository = UserRepository()
