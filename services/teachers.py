from models import Teacher
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from schemas.teachers import TeacherCreate, TeacherUpdate
from services.base import ServiceBase
from repository.teachers import teacher_rep

class TeacherService(ServiceBase[Teacher,TeacherCreate,TeacherUpdate]):
    def __init__(self):
        super().__init__(repository = teacher_rep)

    def get_by_name(self,db:Session,name:str,skip:int = 0,limit:int = 100) ->list[Teacher]:
        teachers = self.repository.get_by_name(db,name = name,skip = skip,limit = limit)
        if not teachers:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with name {name} not found')
        return teachers

    def get_by_department(self,db:Session,department:str,skip:int = 0,limit:int = 100) ->list[Teacher]:
        teachers = self.repository.get_by_department(db, department=department, skip=skip, limit=limit)
        if not teachers:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__} with department {department} not found')
        return teachers

    def get_by_email(self,db:Session,email:str) -> Teacher:
        teacher = self.repository.get_by_email(db,email=email)
        if not teacher:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__}with email {email} not found')
        return teacher

    def create(self, db: Session, data: TeacherCreate) -> Teacher:

        existing_teacher = self.repository.get_by_email(db, email=data.email)
        if existing_teacher:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Teacher with the same email already exist"
            )

        
        return super().create(db, data=data)
teacher_service = TeacherService()