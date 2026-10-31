from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import require_roles
from core.database import get_db
from core.enums import UserRole
from schemas.students import AdminStudentCreate, StudentResponse
from schemas.teachers import AdminTeacherCreate, TeacherResponse
from schemas.users import UserAdminCreate, UserAdminUpdate, UserResponse
from services.students import student_service
from services.teachers import teacher_service
from services.users import user_service

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_roles(UserRole.admin))],
)


@router.get("/users", response_model=Sequence[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    return await user_service.admin_list_users(db, skip=skip, limit=limit)


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserAdminCreate,
    db: AsyncSession = Depends(get_db),
):
    return await user_service.admin_create_user(db, user_in=data)


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    data: UserAdminUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await user_service.admin_update_user(
        db,
        user_id=user_id,
        user_in=data,
    )


@router.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_student_with_user(
    data: AdminStudentCreate,
    db: AsyncSession = Depends(get_db),
):
    return await student_service.admin_create_with_user(db, data)


@router.post(
    "/teachers",
    response_model=TeacherResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_teacher_with_user(
    data: AdminTeacherCreate,
    db: AsyncSession = Depends(get_db),
):
    return await teacher_service.admin_create_with_user(db, data)
