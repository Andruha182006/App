from fastapi import HTTPException,status
from typing import Generic,TypeVar,Sequence
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Base
from repository import CRUDBase

ModelType = TypeVar('ModelType',bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType',bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType',bound=BaseModel)

class ServiceBase(Generic[ModelType,CreateSchemaType,UpdateSchemaType]):
    def __init__(self,repository:CRUDBase[ModelType]):
        self.repository = repository

    async def get_by_id(self,db:AsyncSession,id:int) -> ModelType:
        obj = await self.repository.get_by_id(db,id=id)
        if not obj:
            raise HTTPException(status_code=404,detail=f'{self.repository.model.__name__}not found')
        return obj

    async def get_all(self,db:AsyncSession,skip:int = 0,limit:int = 100) -> Sequence[ModelType]:
        return await self.repository.get_all(db,skip=skip,limit=limit)

    async def create(self,db:AsyncSession,data:CreateSchemaType) -> ModelType:
        return await self.repository.create(db,obj_in_data=data.model_dump())

    async def update(self,db:AsyncSession,id:int,data:UpdateSchemaType) -> ModelType:
        obj =  await self.get_by_id(db,id = id)
        update_data = data.model_dump(exclude_unset=True)
        return await self.repository.update(db,db_obj=obj,update_data=update_data)

    async def delete(self,db:AsyncSession,id:int) -> None:
        await self.get_by_id(db,id=id)
        await self.repository.delete(db,id=id)

