from pydantic import BaseModel, ConfigDict, Field


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


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    student_id: int
    teacher_id: int
