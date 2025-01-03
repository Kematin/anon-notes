from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from src.models.notes import Note, NoteBase
from src.utils.database import DatabaseWorker

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/")
async def get_all_notes():
    worker = DatabaseWorker(Note)
    notes = await worker.get_all()
    return notes


@router.get("/{id}")
async def get_note(id: str):
    # TODO Change to PydanticObjectID
    worker = DatabaseWorker(Note)
    note = await worker.get(id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="note not found."
        )
    return note


@router.post("/")
async def create_note(note_body: NoteBase):
    worker = DatabaseWorker(Note)
    new_doc = Note(text="YO")
    new_doc.create()
    await worker.create(**note_body.model_dump())
