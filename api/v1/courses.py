from fastapi import APIRouter,Depends,status
from schemas.courses import CourseResponse,CourseFilter,CoursesUpdate,CoursesCreate

from sqlalchemy.orm import Session
from core.database import get_db
from services.courses import course_service

router = APIRouter(prefix='/courses',tags=['Courses'])

@router.post('/',response_model=CourseResponse,status_code=status.HTTP_201_CREATED)
def create_course(data:CoursesCreate,db:Session = Depends(get_db)):
    return course_service.create(db,obj_in=data)

@router.get('/',response_model=list[CourseResponse])
def get_courses(filters:CourseFilter = Depends(),skip:int =0,limit:int =100,db:Session = Depends(get_db)):
    if filters.name:
        return course_service.get_by_name(db,name=filters.name,skip=skip,limit=limit)
    if filters.teacher_id:
        return course_service.get_by_teacher_id(db,teacher_id=filters.teacher_id,skip=skip,limit=limit)
    if filters.credits:
        return course_service.get_by_credits(db,credits=filters.credits,skip=skip,limit=limit)

    return course_service.get_multi(db,skip=skip,limit=limit)

@router.patch('/{courser_id}',response_model=CourseResponse)
@router.put('/{courser_id}',response_model=CourseResponse)
def update_course(courser_id:int,data:CoursesUpdate,db:Session = Depends(get_db)):
    db_obj = course_service.get_by_id(db,id=courser_id)
    return course_service.update(db,db_obj=db_obj,obj_in=data)

@router.delete('/{courser_id}',response_model=CourseResponse)
def delete_course(courser_id:int,db:Session = Depends(get_db)):
    return course_service.remove(db,id=courser_id)



