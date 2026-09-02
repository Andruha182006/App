from fastapi import APIRouter,HTTPException
from schemas.students import *

router = APIRouter()

students = {}

@router.get('/students/{student_id}',tags=['Students'])
def read_student(student_id:int):
    if student_id in students:
        return students[student_id]
    else:
        raise HTTPException(status_code=404,detail='Student not found')

@router.post('/students',tags=['Students'])
def create_student(data:StudentCreate):
    student_id = len(students) + 1
    students[student_id] = {
        'id':student_id,
        'name':data.name,
        'age':data.age,
        'email':data.email
    }

    return students[student_id]

@router.put('/students/{student_id}',tags=['Students'])
def put_student(student_id:int,data:StudentUpdate):
    if student_id not in students:
        raise HTTPException(status_code=404,detail='Student not found')
    students[student_id] =  {
        'id':student_id,
        'name':data.name,
        'age':data.age,
        'email': data.email
    }
    return students[student_id]

@router.patch('/students/{student_id}',tags=['Students'])
def patch_student(student_id:int,data:StudentPatch):
    if student_id not in students:
        raise HTTPException(status_code=404, detail='Student not found')
    student = students[student_id]

    if data.name is not None:
        student['name'] = data.name

    if data.age is not None:
        student['age'] = data.age

    if data.email is not None:
        student['email'] = data.email

    return student

@router.delete('/students/{student_id}',tags=['Students'])
def delete_student(student_id:int):
    if student_id in students:
        del students[student_id]
        return {'message': 'Student deleted'}
    else:
        raise HTTPException(status_code=404, detail='Student not found')