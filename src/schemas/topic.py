from datetime import datetime
from uuid import UUID

from schemas import BaseModel


class ListTopic(BaseModel):
    id: UUID
    title: str
    created_at: datetime


class JoinedTopic(BaseModel):
    id: UUID
    title: str


class DetailedTopic(ListTopic):
    pass


class WriteTopicPayload(BaseModel):
    title: str
