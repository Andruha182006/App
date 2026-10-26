from pydantic import BaseModel,ConfigDict

class TeacherSchema(BaseModel):
    name:str
    email:str
    department:str

class TeacherCreate(TeacherSchema):
    pass

class TeacherUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    department: str | None = None

class TeacherFilter(BaseModel):
    name: str|None = None
    email: str|None = None
    department: str|None = None

class TeacherResponse(TeacherSchema):
    model_config = ConfigDict(from_attributes=True)
    id:int
