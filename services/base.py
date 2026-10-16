from fastapi import HTTPException,status
from typing import Generic,TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.database import Base
from repository import CRUDBase

ModelType = TypeVar('ModelType',bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType',bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType',bound=BaseModel)

class ServiceBase(Generic[ModelType,CreateSchemaType,UpdateSchemaType]):
    def __init__(self,repository:CRUDBase[ModelType]):
        self.repository = repository

    def get_by_id(self,db:Session,id:int) -> ModelType:
        obj = self.repository.get_by_id(db,id=id)
        if not obj:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__}not found')
        return obj

    def get_all(self,db:Session,skip:int = 0,limit:int = 100) -> list[ModelType]:
        return self.repository.get_all(db,skip=skip,limit=limit)

    def create(self, db: Session, data: CreateSchemaType) -> ModelType:
        obj_data = data.model_dump()
        db_obj = self.repository.create(db, obj_in_data=obj_data)

        db.commit()  # Фіксуємо транзакцію на рівні бізнес-логіки
        db.refresh(db_obj)  # За потреби оновлюємо стан об'єкта
        return db_obj

    def update(self,db:Session,id:int,data:UpdateSchemaType) -> ModelType:
        db_obj = self.get_by_id(db,id = id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Object not found"
            )
        update_data = data.model_dump(exclude_unset=True)
        return self.repository.update(db,db_obj=db_obj,data=update_data)

    def delete(self,db:Session,id:int) -> None:
        db_obj = self.get_by_id(db,id=id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with id={id} not found"
            )
        self.repository.delete(db,id=id)