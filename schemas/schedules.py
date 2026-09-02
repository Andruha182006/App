from pydantic import BaseModel

class ScheduleSchema(BaseModel):
    day:str
    course_id:int
    teacher_id:int
    group:str
    room:int

class ScheduleCreate(ScheduleSchema):
    pass

class ScheduleUpdate(ScheduleSchema):
    pass

class SchedulePatch(BaseModel):
    day:str|None = None
    course_id:int|None = None
    teacher_id:int|None = None
    group:str|None = None
    room:int|None = None