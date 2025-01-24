from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import status


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_notes(test_client, mock_db_worker, init_test_db):
    mock_instance = Mock()
    mock_instance.get_all = AsyncMock(
        return_value=[
            {"text": b"encrypted1"},
            {"text": b"encrypted2"},
        ]
    )
    mock_db_worker.return_value = mock_instance

    response = await test_client.get("/api/v1/notes/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    mock_instance.get_all.assert_called_once()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_note_success(test_client, mock_db_worker, sample_note):
    mock_instance = Mock()
    mock_instance.get = AsyncMock(return_value=sample_note)
    mock_db_worker.return_value = mock_instance

    with patch("service.crypto.decrypt_content") as mock_decrypt:
        mock_decrypt.return_value = "decrypted content"
        with patch("routers.notes.delete_note_task") as mock_task:
            response = await test_client.get("/api/v1/notes/67939a3a3d6639a9b696c610")

            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == "decrypted content"
            mock_task.delay.assert_called_once_with("67939a3a3d6639a9b696c610")


@pytest.mark.asyncio(loop_scope="session")
async def test_get_note_not_found(test_client, mock_db_worker):
    mock_instance = Mock()
    mock_instance.get = AsyncMock(return_value=None)
    mock_db_worker.return_value = mock_instance

    response = await test_client.get("/api/v1/notes/97939a3a3d6639a9b696c610")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "note not found."


@pytest.mark.asyncio(loop_scope="session")
async def test_create_note(test_client, mock_db_worker, sample_note):
    mock_instance = Mock()
    mock_instance.create = AsyncMock(return_value=sample_note)
    mock_db_worker.return_value = mock_instance

    with patch("service.crypto.encrypt_content") as mock_encrypt:
        mock_encrypt.return_value = b"encrypted_content"

        response = await test_client.post(
            "/api/v1/notes/", json={"text": "test note content"}
        )

        assert response.status_code == status.HTTP_201_CREATED
