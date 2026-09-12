from pydantic import BaseModel,ConfigDict

class StudentSchema(BaseModel):
    name: str
    age: int
    email:str

class StudentCreate(StudentSchema):
    pass

class StudentUpdate(BaseModel):
    name : str|None = None
    age : int|None = None
    email : str|None = None

class StudentResponse(StudentSchema):
    id : int

class StudentFilter(BaseModel):
    name : str|None = None
    age : int|None = None
    email : str|None = None


model_config = ConfigDict(from_attributes=True)

