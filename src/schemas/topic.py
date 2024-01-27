from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, computed_field

from schemas.test import ListTest


class ListTopic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    created_at: datetime


class DetailedTopic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    tests: list[ListTest]
    created_at: datetime


class WriteTopic(BaseModel):
    title: str
