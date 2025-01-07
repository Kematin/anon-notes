import asyncio

from beanie import PydanticObjectId
from loguru import logger
from models import Note
from redis import Redis
from setup import init_db
from utils.database import DatabaseWorker


async def delete_note(note_id: PydanticObjectId, redis: Redis, delay_time: int):
    lock_key = f"processing:note:{note_id}"

    if redis.get(lock_key):
        logger.info(f"Note already in process [ID:{note_id}]")
        return True

    redis.set(lock_key, "processing", ex=delay_time * 60)

    await asyncio.sleep(delay_time * 60)
    await init_db()

    try:
        database = DatabaseWorker(Note)
        await database.delete(note_id)
        logger.info(f"Successfully deleted note [ID:{note_id}]")
        return True
    except Exception as e:
        logger.error(f"Failed to delete note [ID:{note_id}]: {e}")
        return False
    finally:
        redis.delete(lock_key)
