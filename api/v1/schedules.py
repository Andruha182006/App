from fastapi import APIRouter,Depends,status
from schemas.schedules import ScheduleCreate,ScheduleUpdate,ScheduleResponse,ScheduleFilter

from sqlalchemy.orm import Session
from core.database import get_db
from services.schedules import schedule_service

router = APIRouter(prefix='/schedules',tags=['Schedules'])

@router.post('/',response_model=ScheduleResponse,status_code=status.HTTP_201_CREATED)
def create_schedule(data:ScheduleCreate,db:Session = Depends(get_db)):
    return schedule_service.create(db,obj_in=data)

@router.get('/',response_model=list[ScheduleResponse])
def get_schedule(filters:ScheduleFilter = Depends(),skip:int =0,limit:int =100,db:Session = Depends(get_db)):
    if filters.group:
        return schedule_service.get_by_group(db,group=filters.group,skip=skip,limit=limit)
    if filters.room:
        return schedule_service.get_by_room(db,room=filters.room,skip=skip,limit=limit)
    if filters.teacher_id:
        return schedule_service.get_by_teacher_id(db,teacher_id=filters.teacher_id,skip=skip,limit=limit)
    if filters.course_id:
        return schedule_service.get_by_course_id(db,course_id=filters.course_id,skip=skip,limit=limit)

    return schedule_service.get_multi(db,skip=skip,limit=limit)

@router.patch('/{schedule_id}',response_model=ScheduleResponse)
@router.put('/{schedule_id}',response_model=ScheduleResponse)
def update_schedule(schedule_id:int,data:ScheduleUpdate,db:Session = Depends(get_db)):
    db_obj = schedule_service.get_by_id(db,id=schedule_id)
    return schedule_service.update(db,db_obj=db_obj,obj_in=data)

@router.delete('/{schedule_id}',response_model=ScheduleResponse)
def delete_schedule(schedule_id:int,db:Session = Depends(get_db)):
    return schedule_service.remove(db,id=schedule_id)



