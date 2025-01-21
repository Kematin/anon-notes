from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_config
from routers import routers
from setup import configure_logger, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logger(subfolder="fastapi")
    client = await init_db()
    yield
    client.close()


config = get_config()

app = FastAPI(lifespan=lifespan, title="Notes Backend")

for router in routers:
    app.include_router(router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("app:app", host=config.host, port=config.port, reload=config.debug)
