from typing import Type
from uuid import UUID

from fastapi import HTTPException, status

from src.core.exceptions import DatabaseError
from src.crud.note import NoteCrud
from src.models.note import Note
from src.schemas.note import NoteCreatedResponse, NoteCreateSchema, NoteSchema
from src.services.note.note_destroyer import NoteDestroyer


class NoteService:
    crud: Type[NoteCrud] = NoteCrud

    @classmethod
    async def get_one_note_model(cls, id: UUID) -> Note:
        try:
            note = await cls.crud.get_one(id)
        except DatabaseError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with id {id} not found.",
            )
        return note

    @classmethod
    async def create_note(
        cls, note_create_data: NoteCreateSchema
    ) -> NoteCreatedResponse:
        created_id = await cls.crud.create(note_create_data, return_type="id_uuid")
        return NoteCreatedResponse(created_id=created_id)

    @classmethod
    async def get_one_note(cls, id: UUID) -> NoteSchema:
        note = await cls.get_one_note_model(id)
        return_note_schema = NoteSchema(id=id, encrypted_content=note.encrypted_content)
        return return_note_schema

    @classmethod
    async def destroy_note(cls, id: UUID) -> None:
        note = await cls.get_one_note_model(id)
        destroyer = NoteDestroyer(note, cls.crud)
        await destroyer.destroy()
