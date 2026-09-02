from fastapi import APIRouter,HTTPException
from schemas.tasks import *

router = APIRouter()

tasks = {}

@router.post('/tasks',tags=['Tasks'])
def create_task(data:TaskSchema):
    task_id = len(tasks)+1
    tasks[task_id] = {
        'task_id' : task_id,
        'title' : data.title,
        'student_id':data.student_id,
        'teacher_id':data.teacher_id
    }
    return tasks[task_id]

@router.get('/tasks/{task_id}',tags=['Tasks'])
def read_task(task_id:int):
    if task_id in tasks:
        return tasks[task_id]
    else:
        raise HTTPException(status_code=404,detail='Task not found')

@router.put('/tasks/{task_id}',tags=['Tasks'])
def update_task(task_id:int,data:TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail='Task not found')
    tasks[task_id] = {
        'task_id': task_id,
        'title': data.title,
        'student_id': data.student_id,
        'teacher_id': data.teacher_id
    }
    return tasks[task_id]

@router.patch('/tasks/{task_id}',tags=['Tasks'])
def patch_task(task_id:int,data:TaskPatch):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail='Task not found')

    task = tasks[task_id]

    if data.title is not None:
        task['title'] = data.title

    if data.student_id is not None:
        task['student_id'] = data.student_id

    if data.teacher_id is not None:
        task['teacher_id'] = data.teacher_id

    return task

@router.delete('/tasks/{task_id}',tags=['Tasks'])
def delete_task(task_id:int):
    if task_id in tasks:
        del tasks[task_id]
        return {'message':'Task deleted'}
    else:
        raise HTTPException(status_code=404, detail='Task not found')

