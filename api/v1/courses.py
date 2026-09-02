from fastapi import APIRouter,HTTPException
from schemas.courses import*

router = APIRouter()

courses = {}

@router.post('/courses',tags=['Courses'])
def create_course(data:CoursesSchema):
    courser_id = len(courses)+1
    courses[courser_id] = {
        'courser_id':courser_id,
        'name': data.name,
        'credits':data.credits,
        'teacher_id':data.teacher_id
    }
    return courses[courser_id]

@router.get('/courses/{courser_id}',tags=['Courses'])
def read_course(courser_id:int):
    if courser_id in courses:
        return courses[courser_id]
    else:
        raise HTTPException(status_code=404,detail='Course not found')

@router.put('/courses/{courser_id}',tags=['Courses'])
def update_course(courser_id:int,data:CoursesUpdate):
    if courser_id not in courses:
        raise HTTPException(status_code=404, detail='Course not found')
    courses[courser_id] = {
        'courser_id':courser_id,
        'name': data.name,
        'credits': data.credits,
        'teacher_id': data.teacher_id
    }

    return courses[courser_id]

@router.patch('/courses/{courser_id}',tags=['Courses'])
def patch_course(courser_id:int,data:CoursesUpdate):
    if courser_id not in courses:
        raise HTTPException(status_code=404,detail='Course not found')
    course = courses[courser_id]

    if data.name is not None:
        course['name'] = data.name

    if data.credits is not None:
        course['credits'] = data.credits

    if data.teacher_id is not None:
        course['teacher_id'] = data.teacher_id

    return course


@router.delete('/courses/{courser_id}',tags=['Courses'])
def delete_course(courser_id:int):
    if courser_id in courses:
        del courses[courser_id]
        return {'message':'Course deleted'}
    else:
        raise HTTPException(status_code=404,detail='Course not found')



