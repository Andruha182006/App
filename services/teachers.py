from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from repository.teachers import teacher_rep
from schemas.teachers import *
from models.teachers import Teacher

class TeacherService:
    pass