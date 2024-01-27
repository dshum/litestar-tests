from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from pydantic import ConfigDict, computed_field

from schemas import BaseModel
from schemas.test import ListTest


class ListTopic(BaseModel):
    id: UUID
    title: str
    created_at: datetime


class DetailedTopic(BaseModel):
    id: UUID
    title: str
    tests: list[ListTest]
    created_at: datetime


class WriteTopicPayload(BaseModel):
    title: str
