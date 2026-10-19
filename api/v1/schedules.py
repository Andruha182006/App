from fastapi import APIRouter,Depends,status

from schemas.schedules import ScheduleCreate,ScheduleUpdate,ScheduleResponse,ScheduleFilter
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.schedules import schedule_service
from typing import Sequence

router = APIRouter(prefix='/schedules',tags=['Schedules'])

@router.post('/',response_model=ScheduleResponse,status_code=status.HTTP_201_CREATED)
async def create_schedule(data:ScheduleCreate,db:AsyncSession = Depends(get_db)):
    return await schedule_service.create(db,data=data)

@router.get('/',response_model=Sequence[ScheduleResponse])
async def get_schedule(filters:ScheduleFilter = Depends(),skip:int =0,limit:int =100,db:AsyncSession = Depends(get_db)):
    if filters.group:
        return  await schedule_service.get_by_group(db,group=filters.group,skip=skip,limit=limit)

    if filters.room:
        return await schedule_service.get_by_room(db,room=filters.room,skip=skip,limit=limit)

    if filters.teacher_id:
        return await schedule_service.get_by_teacher_id(db,teacher_id=filters.teacher_id,skip=skip,limit=limit)

    if filters.course_id:
        return await schedule_service.get_by_course_id(db,course_id=filters.course_id,skip=skip,limit=limit)

    return await schedule_service.get_all(db,skip=skip,limit=limit)

@router.patch('/{schedule_id}',response_model=ScheduleResponse)
@router.put('/{schedule_id}',response_model=ScheduleResponse)
async def update_schedule(schedule_id:int,data:ScheduleUpdate,db:AsyncSession = Depends(get_db)):
    return await schedule_service.get_by_id(db,id=schedule_id,data=data)


@router.delete('/{schedule_id}',response_model=ScheduleResponse)
async def delete_schedule(schedule_id:int,db:AsyncSession = Depends(get_db)):
     await schedule_service.delete(db,id=schedule_id)



