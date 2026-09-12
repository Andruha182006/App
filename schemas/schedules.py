from pydantic import BaseModel, ConfigDict

class ScheduleSchema(BaseModel):
    day:str
    course_id:int
    teacher_id:int
    group:str
    room:int

class ScheduleCreate(ScheduleSchema):
    pass

class ScheduleUpdate(BaseModel):
    day: str | None = None
    course_id: int | None = None
    teacher_id: int | None = None
    group: str | None = None
    room: int | None = None

class ScheduleResponse(ScheduleSchema):
    id:int

class ScheduleFilter(BaseModel):
    day: str | None = None
    course_id: int | None = None
    teacher_id: int | None = None
    group: str | None = None
    room: int | None = None

model_config = ConfigDict(from_attributes=True)