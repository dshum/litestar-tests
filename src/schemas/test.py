from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ListTest(BaseModel):
    id: UUID
    title: str
    created_at: datetime
