from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.core.config import CONFIG
from src.models import models


async def init_db() -> AsyncIOMotorClient:
    url = "mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_HOST=CONFIG.db.host, DB_PORT=CONFIG.db.port, DB_NAME=CONFIG.db.name
    )
    client: AsyncIOMotorClient = AsyncIOMotorClient(url)
    database: AsyncIOMotorDatabase = client[CONFIG.db.name]

    await init_beanie(database=database, document_models=models)

    return client
