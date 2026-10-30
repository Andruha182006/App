from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentSchema(BaseModel):
    name: str = Field(min_length=1, max_length=25)
    age: int = Field(ge=1, le=150)
    email: EmailStr = Field(max_length=100)


class StudentCreate(StudentSchema):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=25)
    age: int | None = Field(default=None, ge=1, le=150)
    email: EmailStr | None = Field(default=None, max_length=100)


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    email: str


class StudentFilter(BaseModel):
    name: str | None = Field(default=None, max_length=25)
    age: int | None = Field(default=None, ge=0, le=150)
    email: EmailStr | None = Field(default=None, max_length=100)
