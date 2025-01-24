import asyncio

from beanie import PydanticObjectId
from celery import Celery

from config import get_config
from service import jobs
from setup import configure_logger

configure_logger(subfolder="celery")
config = get_config()
celery = Celery(__name__)
celery.conf.update(broker_url=config.celery.url, result_backend=config.celery.url)


@celery.task(name="delete_note")
def delete_note_task(note_id: PydanticObjectId):
    result = asyncio.run(
        jobs.delete_note(note_id, config.celery.redis, config.misc.delete_time)
    )
    return result
