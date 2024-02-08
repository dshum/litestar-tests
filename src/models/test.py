from typing import TYPE_CHECKING, List, Any
from uuid import UUID

from advanced_alchemy import SQLAlchemyAsyncRepository
from advanced_alchemy.base import UUIDAuditBase
from litestar.repository import FilterTypes
from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.service import SQLAlchemyAsyncRepositoryLoggedService
from models.topic import Topic
from models.user_test import UserTest

if TYPE_CHECKING:
    from models import Question


class Test(UUIDAuditBase):
    __tablename__ = "tests"

    title: Mapped[str] = mapped_column(String(255))
    topic_id: Mapped[UUID] = mapped_column(ForeignKey("topics.id", ondelete="restrict"))
    users: Mapped[List["UserTest"]] = relationship(
        foreign_keys="UserTest.test_id",
        back_populates="test",
        lazy="noload",
    )
    topic: Mapped[Topic] = relationship(
        foreign_keys="Test.topic_id",
        back_populates="tests",
        lazy="immediate",
    )
    questions: Mapped[List["Question"]] = relationship(
        foreign_keys="Question.test_id",
        back_populates="test",
        lazy="noload",
    )


class TestRepository(SQLAlchemyAsyncRepository[Test]):
    model_type = Test

    async def get_user_tests(
            self,
            *filters: FilterTypes,
            user_id: UUID,
            **kwargs: Any,
    ) -> tuple[list[Test], int]:
        statement = (
            select(Test)
            .join(UserTest)
            .where(UserTest.user_id == user_id)
        )
        return await self.list_and_count(*filters, statement=statement)

    async def get_user_test(
            self,
            id: UUID,
            user_id: UUID,
    ) -> Test:
        statement = (
            select(Test)
            .join(UserTest)
            .where(UserTest.user_id == user_id)
        )
        return await self.get_one(id=id, statement=statement)


class TestService(SQLAlchemyAsyncRepositoryLoggedService[Test]):
    repository_type = TestRepository

    async def get_user_tests(
            self,
            *filters: FilterTypes,
            user_id: UUID,
            **kwargs: Any,
    ) -> tuple[list[Test], int]:
        return await self.repository.get_user_tests(*filters, user_id=user_id, **kwargs)

    async def get_user_test(
            self,
            id: UUID,
            user_id: UUID,
    ) -> Test:
        return await self.repository.get_user_test(id=id, user_id=user_id)
