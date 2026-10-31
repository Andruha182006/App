from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import get_current_student, get_current_user
from core.database import get_db
from models.students import Student
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
    db: AsyncSession = Depends(get_db),
):
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
    db: AsyncSession = Depends(get_db),
):
    return await task_service.get_by_id(db, id=task_id)


@router.get("/", response_model=Sequence[TaskResponse])
async def read_task(
    filter: TaskFilter = Depends(),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    if filter.title:
        return await task_service.get_by_title(
            db, title=filter.title, skip=skip, limit=limit
        )
    if filter.student_id is not None:
        return await task_service.get_by_student_id(
            db, student_id=filter.student_id, skip=skip, limit=limit
        )
    if filter.teacher_id is not None:
        return await task_service.get_by_teacher_id(
            db, teacher_id=filter.teacher_id, skip=skip, limit=limit
        )

    return await task_service.get_all(db, skip=skip, limit=limit)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await task_service.update(db, id=task_id, data=data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    await task_service.delete(db, id=task_id)
