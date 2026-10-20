from pydantic import BaseModel, ConfigDict

class ScheduleSchema(BaseModel):
    course_id:int
    teacher_id:int
    group:str
    room:int

class ScheduleCreate(ScheduleSchema):
    pass

class ScheduleUpdate(BaseModel):
    course_id: int | None = None
    teacher_id: int | None = None
    group: str | None = None
    room: int | None = None

class ScheduleResponse(ScheduleSchema):
    model_config = ConfigDict(from_attributes=True)
    id:int

class ScheduleFilter(BaseModel):
    course_id: int | None = None
    teacher_id: int | None = None
    group: str | None = None
    room: int | None = None
