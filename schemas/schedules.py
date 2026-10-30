from pydantic import BaseModel, ConfigDict, Field


class ScheduleSchema(BaseModel):
    course_id: int = Field(gt=0)
    teacher_id: int = Field(gt=0)
    group: str = Field(min_length=1, max_length=50)
    room: int = Field(ge=0, le=10000)


class ScheduleCreate(ScheduleSchema):
    pass


class ScheduleUpdate(BaseModel):
    course_id: int | None = Field(default=None, gt=0)
    teacher_id: int | None = Field(default=None, gt=0)
    group: str | None = Field(default=None, min_length=1, max_length=50)
    room: int | None = Field(default=None, ge=0, le=10000)


class ScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    teacher_id: int
    group: str
    room: int


class ScheduleFilter(BaseModel):
    course_id: int | None = Field(default=None, gt=0)
    teacher_id: int | None = Field(default=None, gt=0)
    group: str | None = Field(default=None, max_length=50)
    room: int | None = Field(default=None, ge=0, le=10000)
