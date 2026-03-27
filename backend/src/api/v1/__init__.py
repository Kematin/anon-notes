from fastapi import APIRouter

from src.api.v1.note import router as note_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(note_router)
