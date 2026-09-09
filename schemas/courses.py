from logging import config

from pydantic import BaseModel,ConfigDict

class CoursesSchema(BaseModel):
    name:str
    credits:int
    teacher_id:int

class CoursesCreate(CoursesSchema):
    pass

class CoursesUpdate(CoursesSchema):
    name:str|None = None
    credits:int|None = None
    teacher_id:int|None = None
    
class CourseResponse(CoursesSchema):
    id: int

class CourseFilter(BaseModel):
    name:str|None = None
    credits:int|None = None
    teacher_id:int|None = None

model_config = ConfigDict(from_attributes=True)