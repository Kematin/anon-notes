from uuid import UUID

from fastapi import APIRouter, status

from src.schemas.note import NoteCreateSchema, NoteSchema
from src.services.note import NoteService

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get(
    "/{id}",
    summary="Получить анонимную записку",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": NoteSchema}},
)
async def get_note(id: UUID):
    return await NoteService.get_one_note(id)


@router.delete(
    "/{id}",
    summary="Удалить анонимную записку",
    status_code=status.HTTP_200_OK,
)
async def delete_note(id: UUID):
    await NoteService.destroy_note(id)
    return {"message": "ok"}


@router.post(
    "/",
    summary="Создать новую анонимную записку",
    status_code=status.HTTP_201_CREATED,
)
async def create_note(note_create_schema: NoteCreateSchema):
    return await NoteService.create_note(note_create_schema)
