from fastapi import APIRouter,status
from fastapi.params import Depends

from core.database import get_db
from schemas.students import StudentResponse,StudentFilter,StudentCreate,StudentUpdate
from services.students import student_service
from sqlalchemy.orm import Session

router = APIRouter(prefix='/students',tags =['Students'])

@router.get('/{student_id}',response_model=list[StudentResponse])
def read_student(filter:StudentFilter = Depends(),db:Session = Depends(get_db),skip:int=0,limit:int=100):
    if filter.name:
        return student_service.get_by_name(db,name = filter.name,skip=skip,limit=limit)
    if filter.age:
        return student_service.get_by_age(db,age=filter.age,skip=skip,limit=limit)
    if filter.email:
        return student_service.get_by_email(db,email=filter.email,skip=skip,limit=limit)

    return student_service.get_multi(db,skip,limit)
@router.post('/{student_id}',response_model=StudentResponse,status_code=status.HTTP_201_CREATED)
def create_student(data:StudentCreate,db:Session = Depends(get_db)):
    return student_service.create(db,obj_in=data )

@router.patch('/{student_id}',response_model=StudentResponse)
@router.put('/{student_id}',response_model=StudentResponse)
def put_student(student_id:int,data:StudentUpdate,db:Session = Depends(get_db)):
    db_obj = student_service.get_by_id(db,id = student_id)
    return student_service.update(db,db_obj=db_obj,obj_in=data)

@router.delete('/students/{student_id}',tags=['Students'])
def delete_student(student_id:int,db:Session = Depends(get_db)):
    return student_service.remove(db,id=student_id)