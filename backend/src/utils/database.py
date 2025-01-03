from typing import List, Optional

from beanie import Document, PydanticObjectId
from loguru import logger
from pydantic import BaseModel


class DatabaseWorker[TModel: Document]:
    def __init__(self, model: TModel):
        self.model = model

    async def create(self, **kwargs) -> None:
        logger.debug(kwargs)
        new_document: TModel = self.model(**kwargs)
        await new_document.create()

    async def get(self, id: PydanticObjectId) -> Optional[TModel]:
        doc = await self.model.get(id)
        if doc:
            return doc
        else:
            return False

    async def get_all(self) -> List[TModel]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Optional[TModel]:
        doc = await self.get(id)
        if not doc:
            return False

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
