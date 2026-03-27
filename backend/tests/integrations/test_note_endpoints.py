from uuid import uuid4

import httpx
import pytest
from fastapi import status

from src.api.v1.note import router as note_router
from src.core.exceptions import DatabaseError
from src.crud.note import NoteCrud
from src.schemas.note import NoteCreatedResponse, NoteCreateSchema, NoteSchema
from tests.integrations.conftest import BaseTestRouter


class TestNoteRouter(BaseTestRouter):
    """
    Класс для тестирования src.api.v1.note.router
    """

    router = note_router
    base_route = note_router.prefix

    # MARK: Get
    async def test_get_one_note(
        self,
        note_expires_create_schema: NoteCreateSchema,
        router_client: httpx.AsyncClient,
    ):
        note = await NoteCrud.create(note_expires_create_schema, return_type="model")
        response = await router_client.get(self.base_route + f"/{note.id}")

        assert response.status_code == status.HTTP_200_OK
        response_data = NoteSchema(**response.json())

        assert response_data.id == note.id
        assert response_data.encrypted_content == note.encrypted_content

    async def test_check_not_found_note(self, router_client: httpx.AsyncClient):
        response = await router_client.get(self.base_route + f"/{uuid4()}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # Mark: Post
    async def test_create_note(
        self,
        note_expires_create_schema: NoteCreateSchema,
        router_client: httpx.AsyncClient,
    ):
        request_data = note_expires_create_schema.model_dump(mode="json")
        response = await router_client.post(self.base_route + "/", json=request_data)

        assert response.status_code == status.HTTP_201_CREATED
        response_data = NoteCreatedResponse(**response.json())

        created_note = await NoteCrud.get_one(response_data.created_id)
        assert (
            created_note.encrypted_content
            == note_expires_create_schema.encrypted_content
        )
        assert (
            created_note.timing_for_destroy
            == note_expires_create_schema.timing_for_destroy
        )

    # Mark: Post
    async def test_momentum_delete(
        self,
        note_momentum_destroy_create_schema: NoteCreateSchema,
        router_client: httpx.AsyncClient,
    ):
        note_id = await NoteCrud.create(
            note_momentum_destroy_create_schema, return_type="id_uuid"
        )
        response = await router_client.delete(self.base_route + f"/{note_id}")

        assert response.status_code == status.HTTP_200_OK

        with pytest.raises(DatabaseError):
            await NoteCrud.get_one(note_id)

    async def test_expires_delete(
        self,
        note_expires_create_schema: NoteCreateSchema,
        router_client: httpx.AsyncClient,
    ):
        note_id = await NoteCrud.create(
            note_expires_create_schema, return_type="id_uuid"
        )
        response = await router_client.delete(self.base_route + f"/{note_id}")

        assert response.status_code == status.HTTP_200_OK

        note = await NoteCrud.get_one(note_id)

        assert note.expires_at is not None

    async def test_double_request_expires_delete(
        self,
        note_expires_create_schema: NoteCreateSchema,
        router_client: httpx.AsyncClient,
    ):
        note_id = await NoteCrud.create(
            note_expires_create_schema, return_type="id_uuid"
        )
        await router_client.delete(self.base_route + f"/{note_id}")
        before_note = await NoteCrud.get_one(note_id)

        await router_client.delete(self.base_route + f"/{note_id}")
        after_note = await NoteCrud.get_one(note_id)

        assert after_note.expires_at is not None
        assert after_note.expires_at == before_note.expires_at
