from typing import Generic, Type, TypeVar, Union

import sqlalchemy
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.base import BaseSchema
from shared.database.models.base import AlchemyBaseModel

ModelType = TypeVar("ModelType", bound=AlchemyBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseSchema)
# TODO: update schema support.
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseSchema)


class CrudBase(Generic[ModelType, CreateSchemaType, ReadSchemaType, UpdateSchemaType]):
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.Model = model
        self.db = db

    async def get(self, id: int) -> Union[ModelType, None]:
        try:
            query = sqlalchemy.select(self.Model).where(self.Model.id == id)
            result = await self.db.scalar(query)
            return result
        except AttributeError as e:
            print(f"Error: {e}")
            return None

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.Model(**obj_in_data)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def create_many(self, objs_in: list[CreateSchemaType]) -> list[ModelType]:
        db_objs = []
        for obj_in in objs_in:
            obj_in_data = jsonable_encoder(obj_in)
            db_objs.append(self.Model(**obj_in_data))
        self.db.add_all(db_objs)
        await self.db.commit()
        for db_obj in db_objs:
            await self.db.refresh(db_obj)
        return db_objs

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True, exclude_none=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> ModelType:
        obj = await self.get(id)
        await self.db.delete(obj)
        await self.db.commit()
        return obj
