from fastapi import APIRouter, HTTPException,status,Depends
from schemas.teachers import *
from core.database import get_db
from repository.teachers import teacher_rep

router = APIRouter(prefix='/teachers',tags=['Teachers'])

@router.get('/{teacher_id}',response_model=Еу)
def read_teacher(teacher_id:int):
    if teacher_id in teachers:
        return teachers[teacher_id]
    else:
        raise HTTPException(status_code=404,detail='Teacher not found')

@router.post('/teachers',tags=['Teachers'])
def create_teacher(data:TeacherSchema):
    teacher_id = len(teachers) + 1
    teachers[teacher_id] = {
        'id':teacher_id,
        'name': data.name,
        'email': data.email,
        'department':data.department,
        }

    return teachers[teacher_id]

@router.put('/teachers/{teacher_id}',tags=['Teachers'])
def update_teacher(teacher_id:int,data:TeacherUpdate):
    if teacher_id not in teachers:
        raise HTTPException(status_code=404, detail='Teacher not Found')
    teachers[teacher_id] = {
        'id': teacher_id,
        'name': data.name,
        'email': data.email,
        'department': data.department,
    }
    return teachers[teacher_id]

@router.patch('/teachers/{teacher_id}',tags=['Teachers'])
def patch_teacher(teacher_id:int,data:TeacherPatch):
    teacher = teachers[teacher_id]

    if teacher_id not in teachers:
        raise HTTPException(status_code=404,detail='Teacher not Found')

    if data.name is not None:
        teacher['name'] = data.name

    if data.email is not None:
        teacher['email'] = data.email

    if data.department is not None:
        teacher['department'] = data.department

    return teacher

@router.delete('/teachers/{teacher_id}',tags=['Teachers'])
def delete_teacher(teacher_id:int):
    if teacher_id in teachers:
        del teachers[teacher_id]
        return {'message':'Teacher deleted'}
    else:
        raise HTTPException(status_code=404,detail='Teacher not Found')