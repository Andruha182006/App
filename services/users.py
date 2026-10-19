from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import get_password_hash, verify_password, create_access_token
from models.users import User
from repository.users import UserRepository, user_repository
from schemas.users import UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        existing_user = await self.repo.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        hashed_pwd = get_password_hash(user_in.password)

        return await self.repo.create(db,email=user_in.email,name=user_in.name,
        hashed_password=hashed_pwd)

    async def authenticate_user(self, db: AsyncSession, email: str, password: str) -> str:
        user = await self.repo.get_by_email(db, email=email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account deactivate."
            )

        return create_access_token(subject=user.id)

user_service = UserService(repo=user_repository)