from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from core.enums import TaskStatus


class TaskSchema(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    student_id: int = Field(gt=0)
    teacher_id: int = Field(gt=0)


class TaskCreate(TaskSchema):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    student_id: int | None = Field(default=None, gt=0)
    teacher_id: int | None = Field(default=None, gt=0)


class TaskFilter(BaseModel):
    title: str | None = Field(default=None, max_length=100)
    student_id: int | None = Field(default=None, gt=0)
    teacher_id: int | None = Field(default=None, gt=0)


class TaskSubmit(BaseModel):
    answer: str = Field(min_length=1, max_length=5000)


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    student_id: int
    teacher_id: int
    status: TaskStatus
    answer: str | None = None
    submitted_at: datetime | None = None
