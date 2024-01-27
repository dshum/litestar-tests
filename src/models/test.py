from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.topic import Topic

if TYPE_CHECKING:
    from models import Question


class Test(UUIDAuditBase):
    __tablename__ = "tests"

    title: Mapped[str] = mapped_column(String(255))
    topic_id: Mapped[UUID] = mapped_column(ForeignKey("topics.id", ondelete="restrict"))
    topic: Mapped[Topic] = relationship(
        back_populates="tests",
        foreign_keys="Test.topic_id",
        lazy="noload",
    )
    questions: Mapped[list["Question"]] = relationship(
        back_populates="test",
        lazy="noload",
    )
