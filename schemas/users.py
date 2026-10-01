from uuid import UUID
from typing import Optional

from pydantic import BaseModel,EmailStr,ConfigDict,Field

class UserSchema(BaseModel):
    name:str = Field(...,min_length=2,max_length=100)
    email:EmailStr

class UserCreate(UserSchema):
    password:str = Field(...,min_length=8)

class UserUpdate(BaseModel):
    name:Optional[str] = Field(None,min_length=2,max_length=100)
    email:Optional[EmailStr]=None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id:UUID
    name:str
    email:EmailStr
    is_active:bool