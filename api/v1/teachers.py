from fastapi import APIRouter,status,Depends
from schemas.teachers import *
from core.database import get_db
from sqlalchemy.orm import Session
from services.teachers import teacher_service

router = APIRouter(prefix='/teachers',tags=['Teachers'])

@router.get('/{teacher_id}',response_model=TeacherResponse)
def read_teacher_by_id(teacher_id:int,db:Session = Depends(get_db)):
    return teacher_service.get_by_id(db,id=teacher_id)

@router.get('/',response_model=list[TeacherResponse])
def read_teacher(filter:TeacherFilter = Depends(),db:Session = Depends(get_db),skip:int=0,limit:int=100):
    if filter.name:
        return teacher_service.get_by_name(db,name=filter.name,skip=skip,limit=limit)
    if filter.email:
        return teacher_service.get_by_email(db,email=filter.email,skip=skip,limit=limit)
    if filter.department:
        return teacher_service.get_by_department(db,department=filter.department,skip=skip,limit=limit)

    return teacher_service.get_all(db,skip=skip,limit=limit)

@router.post('/',response_model=TeacherResponse,status_code=status.HTTP_201_CREATED)
def create_teacher(data:TeacherCreate,db:Session = Depends(get_db)):
    return teacher_service.create(db,data=data)

@router.patch('/{teacher_id}',response_model=TeacherResponse)
@router.put('/{teacher_id}',response_model=TeacherResponse)
def update_teacher(teacher_id:int,data:TeacherUpdate,db:Session = Depends(get_db)):
    db_obj = teacher_service.get_by_id(db,id=teacher_id)
    return teacher_service.update(db,id=teacher_id,data=data)

@router.delete('/{teacher_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id:int,db:Session = Depends(get_db)):
    teacher_service.delete(db,id=teacher_id)
    return None