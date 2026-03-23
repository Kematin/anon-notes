from datetime import datetime
from typing import Optional, Self
from uuid import UUID

from pydantic import BaseModel, model_validator

from src.enums.note import TimingForDestroy


class _BaseNoteSchema(BaseModel):
    encrypted_content: str


class NoteSchema(_BaseNoteSchema):
    id: UUID


class NoteCreateSchema(_BaseNoteSchema):
    timing_for_destroy: Optional[TimingForDestroy] = None
    destroy_after_read: bool = False

    @model_validator(mode="after")
    def check_expires_values(self) -> Self:
        error_message = (
            "Only one of the fields (timing_for_destroy, destroy_after_read)"
            + "must be passed to the schema"
        )
        if self.timing_for_destroy is None and self.destroy_after_read is False:
            raise ValueError(error_message)
        if self.timing_for_destroy is not None and self.destroy_after_read is True:
            raise ValueError(error_message)

        return self


class NoteUpdateSchema(BaseModel):
    id: UUID
    expires_at: Optional[datetime]
    destroy_after_read: Optional[bool]
    timing_for_destroy: Optional[TimingForDestroy] = None
