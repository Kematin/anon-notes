from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import status


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_comments(test_client, mock_db_worker_comments, init_test_db):
    mock_instance = Mock()
    mock_instance.get_all = AsyncMock(
        return_value=[
            {"text": "Simple Comment 1", "username": "Anon"},
            {"text": "Simple Comment 2", "username": "test"},
        ]
    )
    mock_db_worker_comments.return_value = mock_instance

    response = await test_client.get("/api/v1/comments/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    mock_instance.get_all.assert_called_once()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_comment(test_client, mock_db_worker_comments, sample_comment):
    mock_instance = Mock()
    mock_instance.create = AsyncMock(return_value=sample_comment)
    mock_db_worker_comments.return_value = mock_instance

    response = await test_client.post(
        "/api/v1/comments/",
        json={"text": sample_comment.text, "username": sample_comment.username},
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["text"] == sample_comment.text
    assert response.json()["username"] == sample_comment.username
    mock_instance.create.assert_called_once()
