from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from src.app import app
from src.enums.note import TimingForDestroy
from src.models.note import Note
from src.schemas.note import NoteCreateSchema, NoteSchema, NoteUpdateSchema


@pytest.fixture
def note():
    with patch.object(Note, "get_settings", return_value=MagicMock()):
        instance = Note(
            id=uuid4(),
            encrypted_content="string",
            destroy_after_read=False,
        )
    return instance


@pytest.fixture
def note_schema():
    return NoteSchema(id=uuid4(), encrypted_content="string")


@pytest.fixture
def note_expires_create_schema():
    return NoteCreateSchema(
        encrypted_content="string",
        timing_for_destroy=TimingForDestroy.MINUTE,
    )


@pytest.fixture
def note_update_schema():
    return NoteUpdateSchema(destroy_after_read=True)


@pytest.fixture
def note_momentum_destroy_create_schema():
    return NoteCreateSchema(
        encrypted_content="string",
        destroy_after_read=True,
    )


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
