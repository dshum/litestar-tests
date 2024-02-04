from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from schemas import BaseModel
from schemas.topic import JoinedTopic

if TYPE_CHECKING:
    from schemas.question import ListQuestion


class ListTest(BaseModel):
    id: UUID
    title: str
    topic: Optional[JoinedTopic]
    created_at: datetime


class JoinedTest(BaseModel):
    id: UUID
    title: str


class DetailedTest(ListTest):
    questions: list["ListQuestion"]


class WriteTestPayload(BaseModel):
    title: str
