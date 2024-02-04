from datetime import datetime
from uuid import UUID

from schemas import BaseModel


class ListQuestion(BaseModel):
    id: UUID
    title: str
    created_at: datetime
