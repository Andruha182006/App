from uuid import UUID
from typing import Optional

from pydantic import BaseModel,EmailStr,ConfigDict,Field

from core.enums import UserRole


class UserSchema(BaseModel):
    name:str = Field(...,min_length=2,max_length=100)
    email:EmailStr

class UserCreate(UserSchema):
    password: str = Field(..., min_length=8, max_length=128)

class UserUpdate(BaseModel):
    name:Optional[str] = Field(None,min_length=2,max_length=100)
    email:Optional[EmailStr]=None

class UserAdminCreate(UserCreate):
    role: UserRole = UserRole.student
    is_active: bool = True

class UserAdminUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:UUID
    name:str|None = None
    email:EmailStr
    is_active:bool
    role:UserRole