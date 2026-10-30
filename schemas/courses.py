from pydantic import BaseModel, ConfigDict, Field


class CoursesSchema(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    credits: int = Field(ge=0, le=100)
    teacher_id: int = Field(gt=0)


class CoursesCreate(CoursesSchema):
    pass


class CoursesUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=50)
    credits: int | None = Field(default=None, ge=0, le=100)
    teacher_id: int | None = Field(default=None, gt=0)


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    credits: int
    teacher_id: int


class CourseFilter(BaseModel):
    title: str | None = Field(default=None, max_length=50)
    credits: int | None = Field(default=None, ge=0, le=100)
    teacher_id: int | None = Field(default=None, gt=0)
