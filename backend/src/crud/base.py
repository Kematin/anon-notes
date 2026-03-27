from typing import Any, Dict, Generic, Literal, Optional, Type, TypeVar, overload
from uuid import UUID

from pydantic import BaseModel

from src.core.exceptions import DatabaseError
from src.models.base import BaseDocument

ModelType = TypeVar("ModelType", bound=BaseDocument)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCrud(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: Type[ModelType]

    @classmethod
    def _return_by_type(
        cls,
        instance: ModelType,
        return_type: Optional[Literal["model", "id_uuid", "id_int"]],
    ) -> Optional[ModelType | UUID | int]:
        if return_type is None:
            return None
        elif return_type in ("id_int", "id_uuid"):
            return instance.id
        else:
            return instance

    @overload
    @classmethod
    async def create(
        cls,
        create_data: CreateSchemaType | Dict[str, Any],
        return_type: Literal["model"] = "model",
    ) -> ModelType: ...

    @overload
    @classmethod
    async def create(
        cls,
        create_data: CreateSchemaType | Dict[str, Any],
        return_type: Literal["id_uuid"],
    ) -> UUID: ...

    @overload
    @classmethod
    async def create(
        cls,
        create_data: CreateSchemaType | Dict[str, Any],
        return_type: Literal["id_int"],
    ) -> int: ...

    @overload
    @classmethod
    async def create(
        cls,
        create_data: CreateSchemaType | Dict[str, Any],
        return_type: None,
    ) -> None: ...

    @classmethod
    async def create(
        cls,
        create_data: CreateSchemaType | Dict[str, Any],
        return_type: Optional[Literal["model", "id_int", "id_uuid"]] = "model",
    ) -> Optional[ModelType | UUID | int]:
        if isinstance(create_data, dict):
            create_data = create_data
        else:
            create_data = create_data.model_dump(exclude_unset=True)

        new_instance = cls.model(**create_data)
        await cls.model.insert_one(new_instance)

        return cls._return_by_type(new_instance, return_type)

    @overload
    @classmethod
    async def update(
        cls,
        instance_id: UUID | int,
        update_data: UpdateSchemaType | Dict[str, Any],
        return_type: Literal["model"] = "model",
    ) -> ModelType: ...

    @overload
    @classmethod
    async def update(
        cls,
        instance_id: UUID | int,
        update_data: UpdateSchemaType | Dict[str, Any],
        return_type: Literal["id_uuid"],
    ) -> UUID: ...

    @overload
    @classmethod
    async def update(
        cls,
        instance_id: UUID | int,
        update_data: UpdateSchemaType | Dict[str, Any],
        return_type: Literal["id_int"],
    ) -> int: ...

    @overload
    @classmethod
    async def update(
        cls,
        instance_id: UUID | int,
        update_data: UpdateSchemaType | Dict[str, Any],
        return_type: None,
    ) -> None: ...

    @classmethod
    async def update(
        cls,
        instance_id: UUID | int,
        update_data: UpdateSchemaType | Dict[str, Any],
        return_type: Optional[Literal["model", "id_int", "id_uuid"]] = "model",
    ) -> Optional[ModelType | UUID | int]:
        if isinstance(update_data, dict):
            update_data = update_data
        else:
            update_data = update_data.model_dump(exclude_unset=True)

        instance = await cls.get_one(instance_id)
        await instance.set(update_data)

        return cls._return_by_type(instance, return_type)

    @classmethod
    async def get_one(cls, instance_id: UUID | int) -> ModelType:
        instance = await cls.model.get(document_id=instance_id)
        if instance is None:
            raise DatabaseError(f"{cls.model.__name__} with id {instance_id} not found")
        return instance

    @classmethod
    async def delete_instance(cls, instance: ModelType) -> None:
        await instance.delete()

    @classmethod
    async def delete_by_id(cls, instance_id: UUID | int) -> None:
        instance = await cls.get_one(instance_id)
        await cls.delete_instance(instance)
