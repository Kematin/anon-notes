from datetime import datetime

from beanie import Document
from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    username: str = "Anon"
    text: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is simple comment!",
            }
        }


class Comment(CommentBase, Document):
    class Settings:
        name = "comments_collection"
