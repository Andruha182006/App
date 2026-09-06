from typing import Any,Generic,Type,TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session
from core.database import Base

ModelType = TypeVar('ModelType',bound=Base)

class CRUDBase(Generic[ModelType]):
    def __init__(self,model:Type[ModelType]):
        self.model = model

    def get_by_id(self,db:Session,id:int) -> ModelType|None:
        return db.get(self.model,id)

    def get_all(self,db:Session,skip:int = 0 ,limit :int = 100 ) -> list[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        return list(db.scalars(query).all())

    def create(self,db:Session,obj_in_data:dict[str,Any]) -> ModelType:
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self,db:Session,db_obj:ModelType,update_data:dict[str,Any]) -> ModelType:
        for field,value in update_data.items():
            if hasattr(db_obj,field):
                setattr(db_obj,field,value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self,db:Session,id:int) -> bool:
        obj = self.get_by_id(db,id)
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True
