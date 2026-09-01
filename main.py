from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

class StudentSchema(BaseModel):
    name: str
    age: int

class StudentCreate(StudentSchema):
    pass

class StudentPatch(BaseModel):
    name : str|None = None
    age : int|None = None

class StudentUpdate(StudentSchema):
    pass

students = {
}

app = FastAPI()

@app.get('/students/{student_id}',tags=['Students'])
def read_student(student_id:int):
    if student_id in students:
        return students[student_id]
    else:
        raise HTTPException(status_code=404,detail='Student not found')

@app.post('/students',tags=['Students'])
def create_student(data:StudentCreate):
    student_id = len(students) + 1
    students[student_id] = {
        'id':student_id,
        'name':data.name,
        'age':data.age,
    }

    return students[student_id]

@app.put('/students/{student_id}',tags=['Students'])
def put_student(student_id:int,data:StudentUpdate):
    students[student_id] =  {
        'id':student_id,
        'name':data.name,
        'age':data.age,
    }
    if student_id not in students:
        raise HTTPException(status_code=404,detail='Student not found')
    return students[student_id]

@app.patch('/students/{student_id}',tags=['Students'])
def patch_student(student_id:int,data:StudentPatch):
    student = students[student_id]
    if data.name is not None:
        student['name'] = data.name

    if data.age is not None:
        student['age'] = data.age

    if student_id not in students:
        raise HTTPException(status_code=404,detail='Student not found')

    return student

@app.delete('/students/{student_id}',tags=['Students'])
def delete_student(student_id:int):
    if student_id in students:
        del students[student_id]
        return {'message': 'Student deleted'}
    else:
        raise HTTPException(status_code=404, detail='Student not found')



teachers = {}

class TeacherSchema(BaseModel):
    name:str
    email:str
    department:str

class TeacherCreate(TeacherSchema):
    pass

class TeacherUpdate(TeacherSchema):
    pass

class TeacherPatch(BaseModel):
    name: str|None = None
    email: str|None = None
    department: str|None = None

@app.get('/teachers/{teacher_id}',tags=['Teachers'])
def read_teacher(teacher_id:int):
    if teacher_id in teachers:
        return teachers[teacher_id]
    else:
        raise HTTPException(status_code=404,detail='Teacher not found')

@app.post('/teachers',tags=['Teachers'])
def create_teacher(data:TeacherSchema):
    teacher_id = len(teachers) + 1
    teachers[teacher_id] = {
        'id':teacher_id,
        'name': data.name,
        'email': data.email,
        'department':data.department,
        }

    return teachers[teacher_id]

@app.put('/teachers/{teacher_id}',tags=['Teachers'])
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

@app.patch('/teachers/{teacher_id}',tags=['Teachers'])
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

@app.delete('/teachers/{teacher_id}',tags=['Teachers'])
def delete_teacher(teacher_id:int):
    if teacher_id in teachers:
        del teachers[teacher_id]
        return {'message':'Teacher deleted'}
    else:
        raise HTTPException(status_code=404,detail='Teacher not Found')


courses = {}

class CoursesSchema(BaseModel):
    name:str
    credits:int

class CoursesCreate(CoursesSchema):
    pass

class CoursesUpdate(CoursesSchema):
    pass

class CoursesPatch(BaseModel):
    name:str|None = None
    credits:int|None = None

@app.post('/courses',tags=['Courses'])
def create_course(data:CoursesSchema):
    courser_id = len(courses)+1
    courses[courser_id] = {
        'courser_id':courser_id,
        'name': data.name,
        'credits':data.credits
    }
    return courses[courser_id]

@app.get('/courses/{courser_id}',tags=['Courses'])
def read_course(courser_id:int):
    if courser_id in courses:
        return courses[courser_id]
    else:
        raise HTTPException(status_code=404,detail='Course not found')

@app.put('/courses/{courser_id}',tags=['Courses'])
def update_course(courser_id:int,data:CoursesUpdate):
    if courser_id not in courses:
        raise HTTPException(status_code=404, detail='Course not found')
    courses[courser_id] = {
        'courser_id':courser_id,
        'name': data.name,
        'credits': data.credits
    }

    return courses[courser_id]

@app.patch('/courses/{courser_id}',tags=['Courses'])
def patch_course(courser_id:int,data:CoursesUpdate):
    if courser_id not in courses:
        raise HTTPException(status_code=404,detail='Course not found')
    course = courses[courser_id]

    if data.name is not None:
        course['name'] = data.name

    if data.credits is not None:
        course['credits'] = data.credits

    return course


@app.delete('/courses/{courser_id}',tags=['Courses'])
def delete_course(courser_id:int):
    if courser_id in courses:
        del courses[courser_id]
        return {'message':'Course deleted'}
    else:
        raise HTTPException(status_code=404,detail='Course not found')



