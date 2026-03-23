from beanie import init_beanie
from motor import motor_asyncio

from src.core.config import CONFIG
from src.model import models


async def init_db() -> motor_asyncio.AsyncIOMotorClient:
    url = "mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_HOST=CONFIG.db.host, DB_PORT=CONFIG.db.port, DB_NAME=CONFIG.db.name
    )
    client = motor_asyncio.AsyncIOMotorClient(url)

    await init_beanie(database=client.db_name, document_models=models)

    return client
