from fastapi import APIRouter,status,Depends

from core.database import get_db
from schemas.tasks import TaskResponse,TaskFilter,TaskCreate,TaskUpdate
from sqlalchemy.orm import Session
from services.tasks import task_service

router = APIRouter(prefix='/tasks',tags=['Tasks'])

@router.post('/tasks',response_model=TaskResponse,status_code=status.HTTP_201_CREATED)
def create_task(data:TaskCreate,db:Session = Depends(get_db)):
    return task_service.create(db,odj_in=data)

@router.get('/{task_id}',response_model=TaskResponse)
def read_task(filter:TaskFilter = Depends(),db:Session = Depends(get_db),skip:int=0,limit:int=100):
    if filter.title:
        return task_service.get_by_title(db,title = filter.title,skip=skip,limit=limit)
    if filter.student_id:
        return task_service.get_by_student_id(db,student_id=filter.student_id,skip=skip,limit=limit)
    if filter.teacher_id:
        return task_service.get_by_teacher_id(db,teacher_id=filter.teacher_id,skip=skip,limit=limit)

    return task_service.get_multi(db,skip=skip,limit=skip)

@router.patch('/{task_id}',response_model=TaskResponse)
@router.put('/{task_id}',response_model=TaskResponse)
def update_task(task_id:int,data:TaskUpdate,db:Session = Depends(get_db)):
    db_obj=task_service.get_by_id(db,id=task_id)
    return task_service.update(db,db_obj=db_obj,obj_in=data)


@router.delete('/tasks/{task_id}',tags=['Tasks'])
def delete_task(task_id:int,db:Session = Depends(get_db)):
    return task_service.remove(db,id=task_id)


