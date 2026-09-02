from fastapi import APIRouter,HTTPException
from schemas.schedules import *

router = APIRouter()

schedules = {}

@router.post('/schedules',tags=['Schedules'])
def create_task(data:ScheduleSchema):
    schedule_id = len(schedules)+1
    schedules[schedule_id] = {
        'day': data.day,
        'course_id': data.course_id,
        'teacher_id': data.teacher_id,
        'group': data.group,
        'room': data.room
    }
    return schedules[schedule_id]

@router.get('/schedules/{schedules_id}',tags=['Schedules'])
def read_task(schedule_id:int):
    if schedule_id in schedules:
        return schedules[schedule_id]
    else:
        raise HTTPException(status_code=404,detail='Schedule not found')

@router.put('/schedules/{schedules_id}',tags=['Schedules'])
def update_task(schedule_id:int,data:ScheduleUpdate):
    if schedule_id not in schedules:
        raise HTTPException(status_code=404, detail='Schedule not found')
    schedules[schedule_id] = {
        'day': data.day,
        'course_id': data.course_id,
        'teacher_id': data.teacher_id,
        'group': data.group,
        'room': data.room
    }
    return schedules[schedule_id]

@router.patch('/schedules/{schedules_id}',tags=['Schedules'])
def patch_task(schedule_id:int,data:SchedulePatch):
    if schedule_id not in schedules:
        raise HTTPException(status_code=404,detail='Schedule not found')

    schedule = schedules[schedule_id]

    if data.day is not None:
        schedule['day'] = data.day

    if data.course_id is not None:
        schedule['course_id'] = data.course_id

    if data.teacher_id is not None:
        schedule['teacher_id'] = data.teacher_id

    if data.group is not None:
        schedule['group'] = data.group

    if data.room is not None:
        schedule['room'] = data.room

    return schedule

@router.delete('/schedules/{schedules_id}',tags=['Schedules'])
def delete_task(schedule_id:int):
    if schedule_id in schedules:
        del schedules[schedule_id]
        return {'message':'Schedule deleted'}
    else:
        raise HTTPException(status_code=404, detail='Schedule not found')