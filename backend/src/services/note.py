from typing import Type
from uuid import UUID

from fastapi import HTTPException, status

from src.crud.note import NoteCrud
from src.model.note import Note
from src.schemas.note import NoteCreateSchema, NoteSchema


class NoteService:
    model: Type[Note] = Note
    crud: Type[NoteCrud] = NoteCrud

    @classmethod
    async def create_note(cls, note_create_data: NoteCreateSchema) -> UUID:
        return await cls.crud.create(note_create_data, return_type="id_uuid")

    @classmethod
    async def get_one_note(cls, id: UUID) -> NoteSchema:
        note = await cls.crud.get_one(id)
        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with id {id} not found.",
            )
        return NoteSchema(id=id, encrypted_content=note.encrypted_content)
