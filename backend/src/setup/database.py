from beanie import init_beanie
from config import config
from models import models
from motor import motor_asyncio


async def init_db() -> motor_asyncio.AsyncIOMotorClient:
    url = "mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_HOST=config.db.host, DB_PORT=config.db.port, DB_NAME=config.db.name
    )
    client = motor_asyncio.AsyncIOMotorClient(url)

    await init_beanie(database=client.db_name, document_models=models)

    return client