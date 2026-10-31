from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TeacherSchema(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=100)
    department: str = Field(min_length=1, max_length=100)


class TeacherCreate(TeacherSchema):
    user_id: UUID | None = None


class AdminTeacherCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=100)
    department: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=128)


class TeacherUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=100)
    department: str | None = Field(default=None, min_length=1, max_length=100)
    user_id: UUID | None = None


class TeacherFilter(BaseModel):
    name: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=100)
    department: str | None = Field(default=None, max_length=100)


class TeacherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    department: str
    user_id: UUID | None = None
