from pydantic import BaseModel

class TaskSchema(BaseModel):
    title:str
    student_id:int
    teacher_id:int

class TaskCreate(TaskSchema):
    pass

class TaskUpdate(TaskSchema):
    pass

class TaskPatch(BaseModel):
    title:str|None = None
    student_id:int|None = None
    teacher_id:int|None = None