from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from beanie import Document
from beanie import PydanticObjectId
from pydantic import BaseModel

TModel = TypeVar("TModel", bound="Document")


class DatabaseWorker(Generic[TModel]):
    def __init__(self, model: type[TModel]):
        self.model = model

    async def create(self, **kwargs) -> TModel:
        new_document: TModel = self.model(**kwargs)
        await new_document.create()
        return new_document

    async def get(self, id: PydanticObjectId) -> Optional[TModel]:
        doc = await self.model.get(id)
        return doc

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[TModel]:
        docs = await self.model.find_all().skip(skip).limit(limit).to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Optional[TModel]:
        doc = await self.get(id)
        if not doc:
            return None

        des_body = body.model_dump()
        des_body = {key: value for key, value in des_body.items() if value is not None}

        update_query = {"$set": {field: value for field, value in des_body.items()}}

        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True


def get_worker():
    from loguru import logger

    async def wrapper(func, *args, **kwargs):
        logger.info("YO")
        return await func(*args, **kwargs)

    return wrapper
