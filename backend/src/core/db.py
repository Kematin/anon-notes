from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.core.config import CONFIG
from src.enums.db import DatabaseCreateType
from src.models import models


async def init_db(
    type: DatabaseCreateType = DatabaseCreateType.MAIN,
) -> AsyncIOMotorClient:

    if type == DatabaseCreateType.MAIN:
        db_host = CONFIG.db.host
        db_port = CONFIG.db.port
        db_name = CONFIG.db.name
    elif type == DatabaseCreateType.TEST:
        db_host = CONFIG.db.host
        db_port = CONFIG.db.port
        db_name = CONFIG.db.test_db_name

    url = _make_database_url(db_host, db_port, db_name)
    client: AsyncIOMotorClient = AsyncIOMotorClient(url)
    database: AsyncIOMotorDatabase = client[db_name]

    await init_beanie(database=database, document_models=models)

    return client


def _make_database_url(db_host: str, db_port: int, db_name: str) -> str:
    return "mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_HOST=db_host, DB_PORT=db_port, DB_NAME=db_name
    )
