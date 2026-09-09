from models import Course
from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository import course_rep
from services.base import ServiceBase
from schemas.courses import CoursesCreate,CoursesUpdate

class CourseService(ServiceBase[Course,CoursesUpdate,CoursesCreate]):
    def __init__(self):
        super().__init__(repository=course_rep)

    def get_by_name(self,db:Session,name:str,skip:int=0,limit:int=100) ->list[Course]:
        courses = self.repository.get_by_name(db,name=name,skip=skip,limit=limit)
        if not courses:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with name{name} not found')
        return courses

    def get_by_credits(self,db:Session,credits:int,skip:int = 0,limit:int=100) ->list[Course]:
        courses = self.repository.get_by_credits(db,credits=credits,skip=skip,limit=limit)
        if not courses:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with how many credits{credits} not found')
        return courses

    def get_course_credits(self,db:Session,course_id:int)->int:
        course = self.get_by_id(db,id=course_id)
        return course.credits

    def get_by_teacher_id(self,db:Session,teacher_id:int,skip:int=0,limit:int=100) -> list[Course]:
        courses = self.repository.get_by_teacher_id(db,teacher_id=teacher_id,skip=skip,limit=limit)
        if not courses:
            raise HTTPException(status_code=404,detail=(f'{self.repository.model.__name__} with teacher{teacher_id} not found'))
        return courses

course_service = CourseService()