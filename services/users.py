from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.enums import UserRole
from core.security import create_access_token, get_password_hash, verify_password
from models.users import User
from repository.users import UserRepository, user_repository
from schemas.users import UserAdminCreate, UserAdminUpdate, UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def _ensure_email_is_free(
        self,
        db: AsyncSession,
        *,
        email: str,
        exclude_user_id: UUID | None = None,
    ) -> None:
        existing_user = await self.repo.get_by_email(db, email=email)
        if existing_user is not None and (
            exclude_user_id is None or existing_user.id != exclude_user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

    async def register_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        await self._ensure_email_is_free(db, email=user_in.email)

        hashed_pwd = get_password_hash(user_in.password)
        return await self.repo.create(
            db,
            email=user_in.email,
            name=user_in.name,
            hashed_password=hashed_pwd,
            role=UserRole.student,
        )

    async def admin_create_user(
        self,
        db: AsyncSession,
        user_in: UserAdminCreate,
    ) -> User:
        await self._ensure_email_is_free(db, email=user_in.email)

        hashed_pwd = get_password_hash(user_in.password)
        return await self.repo.create(
            db,
            email=user_in.email,
            name=user_in.name,
            hashed_password=hashed_pwd,
            role=user_in.role,
            is_active=user_in.is_active,
        )

    async def create_or_promote_admin(
        self,
        db: AsyncSession,
        *,
        email: str,
        name: str,
        password: str,
    ) -> tuple[User, bool]:
        """Create an admin or promote an existing user to admin.

        Returns the user and a flag indicating whether the user was created.
        """
        admin_in = UserAdminCreate(
            name=name,
            email=email,
            password=password,
            role=UserRole.admin,
            is_active=True,
        )
        existing = await self.repo.get_by_email(db, email=str(admin_in.email))

        if existing is not None:
            user = await self.repo.update(
                db,
                user=existing,
                update_data={
                    "role": UserRole.admin,
                    "is_active": True,
                },
            )
            return user, False

        user = await self.repo.create(
            db,
            email=str(admin_in.email),
            name=admin_in.name,
            hashed_password=get_password_hash(admin_in.password),
            role=UserRole.admin,
            is_active=True,
        )
        return user, True

    async def admin_update_user(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        user_in: UserAdminUpdate,
    ) -> User:
        user = await self.repo.get_by_id(db, user_id=user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        update_data = user_in.model_dump(exclude_unset=True)

        new_email = update_data.get("email")
        if new_email is not None:
            await self._ensure_email_is_free(
                db,
                email=str(new_email),
                exclude_user_id=user.id,
            )
            update_data["email"] = str(new_email)

        new_password = update_data.pop("password", None)
        if new_password is not None:
            update_data["hashed_password"] = get_password_hash(new_password)

        if update_data.get("role") is not None:
            update_data["role"] = UserRole(update_data["role"])

        return await self.repo.update(db, user=user, update_data=update_data)

    async def admin_list_users(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ):
        return await self.repo.get_all(db, skip=skip, limit=limit)

    async def authenticate_user(
        self,
        db: AsyncSession,
        email: str,
        password: str,
    ) -> str:
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
                detail="Account deactivate.",
            )

        return create_access_token(subject=user.id)


user_service = UserService(repo=user_repository)
