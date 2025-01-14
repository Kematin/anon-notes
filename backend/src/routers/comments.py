from fastapi import APIRouter
from models.comments import Comment
from models.comments import CommentBase
from utils.database import DatabaseWorker

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/")
async def get_all_comments(skip: int = 0, limit: int = 20):
    worker = DatabaseWorker(Comment)
    comments = await worker.get_all(skip=skip, limit=limit)
    return comments


@router.post("/")
async def create_comment(comment_body: CommentBase):
    worker = DatabaseWorker(Comment)
    comment = await worker.create(**comment_body.model_dump())
    return comment
