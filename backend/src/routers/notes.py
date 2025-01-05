from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from models.notes import Note, NoteBase
from service import crypto
from utils.database import DatabaseWorker

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
    await worker.delete(id)
    return crypto.decrypt_content(note.text)


@router.post("/")
async def create_note(note_body: NoteBase):
    worker = DatabaseWorker(Note)
    note = await worker.create(text=crypto.encrypt_content(note_body.text))
    return note
