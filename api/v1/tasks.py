from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import (
    get_current_student,
    get_current_user,
    load_student_profile,
    load_teacher_profile,
    require_roles,
)
from core.database import get_db
from core.enums import UserRole
from models.students import Student
from models.users import User
from schemas.tasks import (
    TaskCreate,
    TaskFilter,
    TaskResponse,
    TaskSubmit,
    TaskUpdate,
)
from services.tasks import task_service

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    data: TaskCreate,
    current_user: User = Depends(
        require_roles(UserRole.admin, UserRole.teacher)
    ),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if data.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can create tasks only for yourself",
            )
    return await task_service.create(db, data=data)


@router.post("/{task_id}/submit", response_model=TaskResponse)
async def submit_task(
    task_id: int,
    data: TaskSubmit,
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    task = await task_service.get_by_id(db, id=task_id)
    if task.student_id != current_student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can submit only your own tasks",
        )
    return await task_service.submit(db, task=task, answer=data.answer)


@router.get("/{task_id}", response_model=TaskResponse)
async def read_task_by_id(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await task_service.get_by_id(db, id=task_id)

    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if task.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can view only your own tasks",
            )
    elif current_user.role == UserRole.student:
        student = await load_student_profile(db, current_user)
        if task.student_id != student.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can view only your own tasks",
            )

    return task


@router.get("/", response_model=Sequence[TaskResponse])
async def read_task(
    filters: TaskFilter = Depends(),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    student_id = filters.student_id
    teacher_id = filters.teacher_id

    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if teacher_id is not None and teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can view only your own tasks",
            )
        teacher_id = teacher.id
    elif current_user.role == UserRole.student:
        student = await load_student_profile(db, current_user)
        if student_id is not None and student_id != student.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can view only your own tasks",
            )
        student_id = student.id
        teacher_id = filters.teacher_id

    return await task_service.get_filtered(
        db,
        student_id=student_id,
        teacher_id=teacher_id,
        title=filters.title,
        skip=skip,
        limit=limit,
    )


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    current_user: User = Depends(
        require_roles(UserRole.admin, UserRole.teacher)
    ),
    db: AsyncSession = Depends(get_db),
):
    task = await task_service.get_by_id(db, id=task_id)

    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if task.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can update only your own tasks",
            )
        if data.teacher_id is not None and data.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot reassign a task to another teacher",
            )

    return await task_service.update(db, id=task_id, data=data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(
        require_roles(UserRole.admin, UserRole.teacher)
    ),
    db: AsyncSession = Depends(get_db),
):
    task = await task_service.get_by_id(db, id=task_id)

    if current_user.role == UserRole.teacher:
        teacher = await load_teacher_profile(db, current_user)
        if task.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can delete only your own tasks",
            )

    await task_service.delete(db, id=task_id)
