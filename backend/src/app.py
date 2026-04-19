from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.api.v1 import api_v1_router
from src.core.config import CONFIG
from src.core.db import init_db
from src.core.logger import configure_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logger(subfolder="fastapi")
    client = await init_db()
    logger.info("Start app")
    yield
    client.close()
    logger.info("Close app")


app = FastAPI(lifespan=lifespan, title="Notes Backend", redirect_slashes=False)
app.include_router(api_v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("app:app", host=CONFIG.host, port=CONFIG.port, reload=CONFIG.debug)
