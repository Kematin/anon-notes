from fastapi import APIRouter

from src.models.comments import Comment, CommentBase
from src.utils.database import DatabaseWorker

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/")
async def get_all_comments():
    worker = DatabaseWorker(Comment)
    comments = await worker.get_all()
    return comments


@router.post("/")
async def create_comment(comment_body: CommentBase):
    worker = DatabaseWorker(Comment)
    comment = await worker.create(**comment_body.model_dump())
    return comment
