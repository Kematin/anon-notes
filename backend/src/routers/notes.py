from fastapi import APIRouter, HTTPException, status

from models.notes import Note, NoteBase
from service import crypto
from utils.database import DatabaseWorker
from worker import delete_note_task

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
    decrypted_content = crypto.decrypt_content(note.text)
    delete_note_task.delay(id)
    return decrypted_content


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_note(note_body: NoteBase):
    worker = DatabaseWorker(Note)
    note = await worker.create(text=crypto.encrypt_content(note_body.text))
    return note
