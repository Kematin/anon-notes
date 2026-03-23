from typing import Any, Dict, Generic, Literal, Optional, Type, TypeVar, overload
from uuid import UUID

from beanie import Document
from pydantic import BaseModel

ModelType = TypeVar("DocumentType", bound=Document)
CreateShemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateShemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCrud(Generic[ModelType, CreateShemaType, UpdateShemaType]):
    model: Type[ModelType]

    @overload
    @classmethod
    async def create(
        cls,
        create_data: CreateShemaType | Dict[str, Any],
        return_type: Literal["model"] = "model",
    ) -> ModelType: ...

    @overload
    @classmethod
    async def create(
        cls,
        create_data: CreateShemaType | Dict[str, Any],
        return_type: Literal["id_uuid"],
    ) -> UUID: ...

    @overload
    @classmethod
    async def create(
        cls,
        create_data: CreateShemaType | Dict[str, Any],
        return_type: Literal["id_int"],
    ) -> int: ...

    @overload
    @classmethod
    async def create(
        cls,
        create_data: CreateShemaType | Dict[str, Any],
        return_type: None,
    ) -> None: ...

    @classmethod
    async def create(
        cls,
        create_data: CreateShemaType | Dict[str, Any],
        return_type: Optional[Literal["model", "id_int", "id_uuid"]],
    ) -> Optional[ModelType | UUID | int]:
        if isinstance(create_data, dict):
            create_data = create_data
        else:
            create_data = create_data.model_dump(exclude_unset=True)

        new_instance = cls.model(**create_data)
        await cls.model.insert_one(new_instance)

        if return_type is None:
            return None
        elif return_type in ("id_int", "id_uuid"):
            return new_instance.id
        else:
            return new_instance

    @overload
    @classmethod
    async def update(
        cls, update_data: UpdateShemaType | Dict[str, Any]
    ) -> ModelType: ...

    @classmethod
    async def get_one(cls, instance_id: UUID) -> ModelType:
        return await cls.model.get(document_id=instance_id)
