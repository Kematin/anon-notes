from src.crud.base import BaseCrud
from src.model.note import Note
from src.schemas.note import NoteCreateSchema, NoteUpdateSchema


class NoteCrud(BaseCrud[Note, NoteCreateSchema, NoteUpdateSchema]):
    model = Note
