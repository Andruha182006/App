from collections.abc import Callable
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import get_db
from core.enums import UserRole
from models.students import Student
from models.teachers import Teacher
from models.users import User
from repository.students import student_rep
from repository.teachers import teacher_rep
from repository.users import user_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(db: AsyncSession = Depends(get_db),token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate the authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = UUID(user_id_str)
    except (jwt.PyJWTError, ValueError):
        raise credentials_exception

    user = await user_repository.get_by_id(db, user_id=user_id)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_roles(*roles: UserRole) -> Callable:
    async def checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return checker


async def load_student_profile(db: AsyncSession, user: User) -> Student:
    student = await student_rep.get_by_user_id(db, user_id=user.id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student profile is not linked to this account",
        )
    return student


async def load_teacher_profile(db: AsyncSession, user: User) -> Teacher:
    teacher = await teacher_rep.get_by_user_id(db, user_id=user.id)
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher profile is not linked to this account",
        )
    return teacher


async def get_current_student(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.student)),
) -> Student:
    return await load_student_profile(db, current_user)


async def get_current_teacher(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.teacher)),
) -> Teacher:
    return await load_teacher_profile(db, current_user)