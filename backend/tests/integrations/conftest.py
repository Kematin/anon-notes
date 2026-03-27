from typing import AsyncGenerator

import httpx
import pytest_asyncio
from fastapi import APIRouter, FastAPI


class BaseTestRouter:
    router: APIRouter
    base_route: str

    @pytest_asyncio.fixture(scope="function")
    async def router_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """
        Настривает `httpx.AsyncClient` для перенправления запросов напрямую в
        API с использованием протокола ASGI

        Returns:
            AsyncGenerator[httpx.AsyncClient, None]:
            Асинхронный генератор для экземпляра `httpx.AsyncClient`
        """

        app = FastAPI()
        app.include_router(self.router)

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://test"
        ) as async_client:
            yield async_client
