from fastapi import APIRouter,status,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas.tasks import TaskResponse,TaskFilter,TaskCreate,TaskUpdate
from services.tasks import task_service
from typing import Sequence

router = APIRouter(prefix='/tasks',tags=['Tasks'])

@router.post('/',response_model=TaskResponse,status_code=status.HTTP_201_CREATED)
async def create_task(data:TaskCreate,db:AsyncSession = Depends(get_db)):
    return await task_service.create(db,data=data)

@router.get('/{task_id}',response_model=TaskResponse)
async def read_task_by_id(task_id:int,db:AsyncSession = Depends(get_db)):
    return await task_service.get_by_id(db,id=task_id)

@router.get('/',response_model=Sequence[TaskResponse])
async def read_task(filter:TaskFilter = Depends(),db:AsyncSession = Depends(get_db),skip:int=0,limit:int=100):
    if filter.title:
        return await task_service.get_by_title(db,title = filter.title,skip=skip,limit=limit)
    if filter.student_id is not None:
        return await task_service.get_by_student_id(db,student_id=filter.student_id,skip=skip,limit=limit)
    if filter.teacher_id is not None:
        return await task_service.get_by_teacher_id(db,teacher_id=filter.teacher_id,skip=skip,limit=limit)

    return await task_service.get_all(db,skip=skip,limit=limit)

@router.patch('/{task_id}',response_model=TaskResponse)
async def update_task(task_id:int,data:TaskUpdate,db:AsyncSession = Depends(get_db)):
    return await task_service.update(db,id=task_id,data=data)


@router.delete('/{task_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id:int,db:AsyncSession = Depends(get_db)):
    await task_service.delete(db,id=task_id)



