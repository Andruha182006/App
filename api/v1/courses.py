from fastapi import APIRouter,Depends,status
from schemas.courses import CourseResponse,CourseFilter,CoursesUpdate,CoursesCreate
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.courses import course_service

router = APIRouter(prefix='/courses',tags=['Courses'])

@router.post('/',response_model=CourseResponse,status_code=status.HTTP_201_CREATED)
async def create_course(data:CoursesCreate,db:AsyncSession = Depends(get_db)):
    return await course_service.create(db,data=data)

@router.get('/{course_id}',response_model=CourseResponse)
async def read_course_by_id(course_id:int,db:AsyncSession = Depends(get_db)):
    return await course_service.get_by_id(db,id=course_id)

@router.get('/',response_model=Sequence[CourseResponse])
async def get_courses(filters:CourseFilter = Depends(),skip:int =0,limit:int =100,db:AsyncSession = Depends(get_db)):
    if filters.name:
        course = await course_service.get_by_name(db,name=filters.name,skip=skip,limit=limit)
        return [course] if course else []
    if filters.teacher_id:
        course = await course_service.get_by_teacher_id(db,teacher_id=filters.teacher_id,skip=skip,limit=limit)
        return [course] if course else []
    if filters.credits:
        course = await course_service.get_by_credits(db,credits=filters.credits,skip=skip,limit=limit)
        return [course] if course else []

    return course_service.get_all(db,skip=skip,limit=limit)

@router.patch('/{courser_id}',response_model=CourseResponse)
async def update_course(course_id:int,data:CoursesUpdate,db:AsyncSession = Depends(get_db)):
    return await course_service.update(db,id=course_id,data=data)

@router.delete('/{courser_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id:int,db:AsyncSession = Depends(get_db)):
    await course_service.delete(db,id=course_id)




