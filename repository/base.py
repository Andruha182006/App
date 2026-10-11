from typing import Any,Generic,Type,TypeVar,Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import Base

ModelType = TypeVar('ModelType',bound=Base)

class CRUDBase(Generic[ModelType]):
    def __init__(self,model:Type[ModelType]):
        self.model = model

    async def get_by_id(self,db:AsyncSession,id:int) -> ModelType|None:
        return await db.get(self.model,id)

    async def get_all(self,db:AsyncSession,skip:int = 0 ,limit :int = 100 ) -> Sequence[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(self,db:AsyncSession,obj_in_data:dict[str,Any]) -> ModelType:
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self,db:AsyncSession,db_obj:ModelType,update_data:dict[str,Any]) -> ModelType:
        for field,value in update_data.items():
            if hasattr(db_obj,field):
                setattr(db_obj,field,value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self,db:AsyncSession, id:int) -> bool:
        obj = await self.get_by_id(db,id)
        if not obj:
            return False
        await db.delete(obj)
        await db.commit()
        return True
