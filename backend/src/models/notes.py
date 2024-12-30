from datetime import datetime

from beanie import Document


class Note(Document):
    text: str
    created_at: datetime = datetime.now

    class Settings:
        name = "notes_collection"

    class Config:
        schema_extra = {
            "example": {"text": "This is secret note!", "created_at": datetime.now()}
        }
