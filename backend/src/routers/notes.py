from fastapi import APIRouter
from loguru import logger

from models.notes import Note, NoteBase
from utils.database import DatabaseWorker

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/{uuid}")
async def get_note(uuid: str):
    return f"hello {uuid}"


@router.post("/")
async def create_note(note_body: NoteBase):
    pass
