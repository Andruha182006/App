from pydantic import BaseModel

class CoursesSchema(BaseModel):
    name:str
    credits:int
    teacher_id:int

class CoursesCreate(CoursesSchema):
    pass

class CoursesUpdate(CoursesSchema):
    pass

class CoursesPatch(BaseModel):
    name:str|None = None
    credits:int|None = None
    teacher_id:int|None = None