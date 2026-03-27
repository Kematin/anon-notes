from datetime import datetime
from typing import Optional

from pymongo import IndexModel

from src.enums.note import TimingForDestroy
from src.models.base import BaseDocument


class Note(BaseDocument):
    encrypted_content: str
    expires_at: Optional[datetime] = None
    timing_for_destroy: Optional[TimingForDestroy] = None
    destroy_after_read: bool = False

    class Settings:
        name = "notes_collection"
        indexes = [IndexModel([("expires_at", 1)], expireAfterSeconds=0)]
