from typing import Generator
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from src.core.config import CONFIG
from src.core.db import init_db
from src.crud.note import NoteCrud
from src.enums.db import DatabaseCreateType
from src.enums.note import TimingForDestroy
from src.models.note import Note
from src.schemas.note import NoteCreateSchema, NoteSchema, NoteUpdateSchema


# MARK: DB
@pytest.fixture(scope="session", autouse=True)
async def test_db():
    client = await init_db(DatabaseCreateType.TEST)
    yield client
    client.drop_database(CONFIG.db.test_db_name)
    client.close()


# MARK: Note
@pytest.fixture
def note() -> Note:
    instance = Note(
        id=uuid4(),
        encrypted_content="string",
        destroy_after_read=False,
    )
    return instance


@pytest.fixture
def note_schema() -> NoteSchema:
    return NoteSchema(id=uuid4(), encrypted_content="string")


@pytest.fixture
def note_expires_create_schema() -> NoteCreateSchema:
    return NoteCreateSchema(
        encrypted_content="string",
        timing_for_destroy=TimingForDestroy.MINUTE,
    )


@pytest.fixture
def note_momentum_destroy_create_schema() -> NoteCreateSchema:
    return NoteCreateSchema(
        encrypted_content="string",
        destroy_after_read=True,
    )


@pytest.fixture
def note_update_schema() -> NoteUpdateSchema:
    return NoteUpdateSchema(destroy_after_read=True)


@pytest.fixture
def note_crud() -> Generator[NoteCrud]:
    with patch.object(NoteCrud, "model") as mock_model:
        mock_model.insert_one = AsyncMock()
        yield mock_model
