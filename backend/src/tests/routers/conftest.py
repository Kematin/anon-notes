from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from app import app
from models import Comment, Note
from setup import init_db


@pytest.fixture(scope="session")
async def init_test_db():
    client = await init_db()
    test_db = client["notes_test"]
    yield test_db
    await test_db.drop_collection(Note.get_collection_name())
    await test_db.drop_collection(Comment.get_collection_name())
    client.close()


@pytest.fixture(scope="session")
async def test_client(init_test_db):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def mock_db_worker():
    with (
        patch("routers.notes.DatabaseWorker") as mock,
    ):
        yield mock


@pytest.fixture
def mock_db_worker_comments():
    with (
        patch("routers.comments.DatabaseWorker") as mock,
    ):
        yield mock


@pytest.fixture
def sample_note():
    return Note(id="67939a3a3d6639a9b696c610", text=b"encrypted_content")


@pytest.fixture
def sample_comment():
    return Comment(
        id="37939a3a3d6639a9b696c610", text="Simple Comment", username="test"
    )
