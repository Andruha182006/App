from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.users import User

class UserRepository:
    async def get_by_id(self, db: AsyncSession, user_id: UUID) -> Optional[User]:
        return await db.get(User,user_id)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result =  await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, email: str, name: str, hashed_password: str) -> User:
        db_user = User(email=email,name=name,hashed_password=hashed_password,is_active=True)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

user_repository = UserRepository()