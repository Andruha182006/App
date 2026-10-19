from pydantic import BaseModel,ConfigDict

class CoursesSchema(BaseModel):
    title:str
    credits:int
    teacher_id:int

class CoursesCreate(CoursesSchema):
    pass

class CoursesUpdate(CoursesSchema):
    title:str|None = None
    credits:int|None = None
    teacher_id:int|None = None

class CourseResponse(CoursesSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int

class CourseFilter(BaseModel):
    title:str|None = None
    credits:int|None = None
    teacher_id:int|None = None

