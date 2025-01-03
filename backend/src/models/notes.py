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
                "created_at": datetime.now(),
            }
        }


class Note(NoteBase, Document):
    _id: str
