from pydantic import BaseModel

class TeacherSchema(BaseModel):
    name:str
    email:str
    department:str

class TeacherCreate(TeacherSchema):
    pass

class TeacherUpdate(TeacherSchema):
    pass

class TeacherPatch(BaseModel):
    name: str|None = None
    email: str|None = None
    department: str|None = None