from fastapi import APIRouter,status,Depends

from core.database import get_db
from schemas.students import StudentResponse,StudentFilter,StudentCreate,StudentUpdate
from services.students import student_service
from sqlalchemy.orm import Session

router = APIRouter(prefix='/students',tags =['Students'])

@router.get('/{student_id}',response_model=StudentResponse)
def get_student_by_id(student_id:int,db:Session = Depends(get_db)):
    return student_service.get_by_id(db,id=student_id)

@router.get('/',response_model=list[StudentResponse])
def read_student(filter:StudentFilter = Depends(),db:Session = Depends(get_db),skip:int=0,limit:int=100):
    if filter.name:
        return student_service.get_by_name(db,name = filter.name,skip=skip,limit=limit)
    if filter.age:
        return student_service.get_by_age(db,age=filter.age,skip=skip,limit=limit)
    if filter.email:
        return student_service.get_by_email(db,email=filter.email,skip=skip,limit=limit)

    return student_service.get_all(db,skip=skip,limit=limit)

@router.post('/',response_model=StudentResponse,status_code=status.HTTP_201_CREATED)
def create_student(data:StudentCreate,db:Session = Depends(get_db)):
    return student_service.create(db,data=data)

@router.patch('/{student_id}',response_model=StudentResponse)
@router.put('/{student_id}',response_model=StudentResponse)
def update_student(student_id:int,data:StudentUpdate,db:Session = Depends(get_db)):
    return student_service.update(db,id=student_id,data=data)

@router.delete('/{student_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id:int,db:Session = Depends(get_db)):
    student_service.delete(db,id=student_id)
    return None