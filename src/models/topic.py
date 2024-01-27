from typing import TYPE_CHECKING, Any

from advanced_alchemy import SQLAlchemyAsyncRepository
from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.service import SQLAlchemyAsyncRepositoryService
from schemas.topic import ListTopic

if TYPE_CHECKING:
    from models import Test


class Topic(UUIDAuditBase):
    __tablename__ = "topics"

    title: Mapped[str] = mapped_column(String(255))
    tests: Mapped[list["Test"]] = relationship(
        back_populates="topic",
        innerjoin=True,
        lazy="noload",
    )


class TopicRepository(SQLAlchemyAsyncRepository[Topic]):
    model_type = Topic


class TopicService(SQLAlchemyAsyncRepositoryService[Topic]):
    repository_type = TopicRepository
