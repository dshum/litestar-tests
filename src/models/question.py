from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.test import Test


class Question(UUIDAuditBase):
    __tablename__ = "questions"

    question: Mapped[str] = mapped_column(Text)
    test_id: Mapped[UUID] = mapped_column(ForeignKey("tests.id", ondelete="restrict"))
    test: Mapped[Test] = relationship(
        back_populates="questions",
        foreign_keys="Question.test_id",
        lazy="noload",
    )
