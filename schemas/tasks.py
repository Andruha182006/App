from pydantic import BaseModel, ConfigDict

class TaskSchema(BaseModel):
    title:str
    student_id:int
    teacher_id:int

class TaskCreate(TaskSchema):
    pass

class TaskUpdate(TaskSchema):
    title: str | None = None
    student_id: int | None = None
    teacher_id: int | None = None

class TaskFilter(BaseModel):
    title:str|None = None
    student_id:int|None = None
    teacher_id:int|None = None

class TaskResponse(TaskSchema):
    id:int

model_config = ConfigDict(from_attributes=True)