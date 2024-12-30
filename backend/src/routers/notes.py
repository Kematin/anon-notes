from fastapi import APIRouter

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/")
async def get_note():
    return "hello"
