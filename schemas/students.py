from pydantic import BaseModel

class StudentSchema(BaseModel):
    name: str
    age: int
    email:str

class StudentCreate(StudentSchema):
    pass

class StudentPatch(BaseModel):
    name : str|None = None
    age : int|None = None
    email : str|None = None

class StudentUpdate(StudentSchema):
    pass