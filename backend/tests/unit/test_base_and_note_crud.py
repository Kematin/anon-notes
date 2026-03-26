from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from src.core.exceptions import DatabaseError
from src.crud.note import NoteCrud
from src.models.note import Note

# =========================================
# Mark: Local Fixtures
# =========================================


@pytest.fixture
def mock_note_crud():
    with patch.object(NoteCrud, "model") as mock_model:
        mock_model.insert_one = AsyncMock()
        yield mock_model


# =========================================
# Mark: Get
# =========================================


@pytest.mark.asyncio
async def test_crud_get_one_id(note, mock_note_crud):
    mock_note_crud.get = AsyncMock(return_value=note)
    result = await NoteCrud.get_one(note.id)

    assert result == note
    assert result.id == note.id


@pytest.mark.asyncio
async def test_negative_crud_get_one(note, mock_note_crud):
    mock_note_crud.get = AsyncMock(return_value=None)
    mock_note_crud.__name__ = "NoteCrud"
    with pytest.raises(DatabaseError):
        await NoteCrud.get_one(uuid4())


# =========================================
# Mark: Create
# =========================================


@pytest.mark.asyncio
async def test_crud_create_return_id(note_expires_create_schema, note, mock_note_crud):
    mock_note_crud.return_value = note
    result = await NoteCrud.create(note_expires_create_schema, return_type="id_uuid")
    assert result == note.id


@pytest.mark.asyncio
async def test_crud_create_return_model(
    note_expires_create_schema, note, mock_note_crud
):
    mock_note_crud.return_value = note
    result = await NoteCrud.create(note_expires_create_schema, return_type="model")
    assert result == note


@pytest.mark.asyncio
async def test_crud_create_return_none(note_expires_create_schema, note, mock_note_crud):
    mock_note_crud.return_value = note
    result = await NoteCrud.create(note_expires_create_schema, return_type=None)
    assert result is None


@pytest.mark.asyncio
async def test_crud_create_with_simple_data(note, mock_note_crud):
    create_data = {
        "encrypted_content": "string",
        "delete_after_read": True,
    }
    mock_note_crud.return_value = note
    result = await NoteCrud.create(create_data, return_type="id_uuid")
    assert result == note.id


# =========================================
# Mark: Update
# =========================================


@pytest.mark.asyncio
async def test_crud_update(note, note_update_schema):
    with patch.object(NoteCrud, "get_one", new=AsyncMock(return_value=note)):
        with patch.object(Note, "set", new=AsyncMock(return_value=None)) as mock_set:
            result = await NoteCrud.update(
                note.id, note_update_schema, return_type="model"
            )

    assert result == note
    mock_set.assert_called_once_with({"destroy_after_read": True})


@pytest.mark.asyncio
async def test_update_with_simple_data(note):
    update_data = {
        "destroy_after_read": True,
    }

    with patch.object(NoteCrud, "get_one", new=AsyncMock(return_value=note)):
        with patch.object(Note, "set", new=AsyncMock(return_value=None)) as mock_set:
            result = await NoteCrud.update(note.id, update_data, return_type="model")

    assert result == note
    mock_set.assert_called_once_with({"destroy_after_read": True})


# =========================================
# Mark: Delete
# =========================================


@pytest.mark.asyncio
async def test_crud_delete(note):
    with patch.object(Note, "delete", new=AsyncMock(return_value=None)) as mock_delete:
        result = await NoteCrud.delete_instance(note)

    mock_delete.assert_called_once()
    assert result is None


@pytest.mark.asyncio
async def test_crud_delete_by_id(note):
    with patch.object(NoteCrud, "get_one", new=AsyncMock(return_value=note)):
        with patch.object(
            Note, "delete", new=AsyncMock(return_value=None)
        ) as mock_delete:
            result = await NoteCrud.delete_by_id(note.id)

    mock_delete.assert_called_once()
    assert result is None
