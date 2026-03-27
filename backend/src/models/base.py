from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field


class BaseDocument(Document):
    id: UUID = Field(default_factory=uuid4)
