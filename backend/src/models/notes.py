from datetime import datetime

from beanie import Document
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    text: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is a secret note! (encrypted)",
            }
        }


class Note(NoteBase, Document):
    class Settings:
        name = "notes_collection"
