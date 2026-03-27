from datetime import datetime, timedelta, timezone
from typing import Type

from loguru import logger

from src.core.exceptions import ServiceError
from src.crud.note import NoteCrud
from src.enums.note import TimingForDestroy
from src.models.note import Note
from src.schemas.note import NoteUpdateSchema


class NoteDestroyer:
    def __init__(self, note: Note, crud: Type[NoteCrud]):
        self.note = note
        self.crud = crud

    async def destroy(self) -> None:
        if self.note.destroy_after_read:
            await self._destroy_instantly(self.note)
        elif self.note.timing_for_destroy:
            await self._destroy_after_timing(self.note)

    async def _destroy_instantly(self, note: Note) -> None:
        await self.crud.delete_instance(note)

    async def _destroy_after_timing(self, note: Note) -> None:
        if self.note.expires_at:
            logger.info(f"Note ({self.note.id}) already have expires_at field")
            return

        if note.timing_for_destroy is None:
            raise ServiceError(
                f"Note ({self.note.id}) doesnt have timing_for_destroy field"
            )

        update_schema = NoteUpdateSchema(
            expires_at=self._get_expires_at(note.timing_for_destroy)
        )
        await self.crud.update(
            instance_id=note.id, update_data=update_schema, return_type=None
        )

    def _get_expires_at(self, timing: TimingForDestroy) -> datetime:
        match timing:
            case TimingForDestroy.MINUTE:
                minutes = 1
            case TimingForDestroy.HOUR:
                minutes = 60
            case TimingForDestroy.DAY:
                minutes = 60 * 24
            case TimingForDestroy.WEEK:
                minutes = 60 * 24 * 7

        return datetime.now(tz=timezone.utc) + timedelta(minutes=minutes)
