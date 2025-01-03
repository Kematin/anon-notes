from datetime import datetime

from beanie import Document


class Comment(Document):
    username: str = "Anon"
    text: str
    created_at: datetime = datetime.now

    class Settings:
        name = "comments_collection"

    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is simple comment!",
                "created_at": datetime.now(),
            }
        }
