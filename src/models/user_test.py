from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDBase
from advanced_alchemy.types import DateTimeUTC
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from models import Test, User


class UserTest(UUIDBase):
    __tablename__ = "users_tests_pivot"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    test_id: Mapped[UUID] = mapped_column(ForeignKey("tests.id"), primary_key=True)
    creator_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    test: Mapped["Test"] = relationship(
        back_populates="users",
    )
    user: Mapped["User"] = relationship(
        foreign_keys=[user_id],
        back_populates="tests",
    )
    creator_user: Mapped["User"] = relationship(
        foreign_keys=[creator_user_id],
        back_populates="assigned_tests",
    )
