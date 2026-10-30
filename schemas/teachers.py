from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TeacherSchema(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=100)
    department: str = Field(min_length=1, max_length=100)


class TeacherCreate(TeacherSchema):
    pass


class TeacherUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=100)
    department: str | None = Field(default=None, min_length=1, max_length=100)


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
