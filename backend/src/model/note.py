from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field
from pymongo import IndexModel

from src.enums.note import TimingForDestroy


class Note(Document):
    id: UUID = Field(default_factory=uuid4)
    encrypted_content: str
    expires_at: Optional[datetime] = None
    timing_for_destroy: Optional[TimingForDestroy] = None
    destroy_after_read: bool = False

    class Settings:
        name = "notes_collection"
        indexes = [IndexModel([("expires_at", 1)], expireAfterSeconds=0)]
