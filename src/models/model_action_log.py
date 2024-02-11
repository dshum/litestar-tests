import json
from enum import Enum
from typing import Any, TYPE_CHECKING
from uuid import UUID

from advanced_alchemy import SQLAlchemyAsyncRepository, SQLAlchemyAsyncRepositoryService, ModelT
from advanced_alchemy.base import UUIDAuditBase
from litestar import Request
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.sqlalchemy_encoding import SQLAlchemyEncoder

if TYPE_CHECKING:
    from models import User


class ActionType(str, Enum):
    CREATE = "Create"
    UPDATE = "Update"
    DELETE = "Delete"


class ModelActionLog(UUIDAuditBase):
    __tablename__ = "model_action_logs"

    model_name: Mapped[str] = mapped_column(String(255))
    object_id: Mapped[UUID | None] = mapped_column()
    action: Mapped[ActionType | None] = mapped_column(default=None)
    data: Mapped[str | None] = mapped_column(Text, default=None)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="restrict"))
    user: Mapped["User"] = relationship(
        foreign_keys="ModelActionLog.user_id",
        lazy="noload",
    )


class ModelActionLogRepository(SQLAlchemyAsyncRepository[ModelActionLog]):
    model_type = ModelActionLog


class ModelActionLogService(SQLAlchemyAsyncRepositoryService[ModelActionLog]):
    repository_type = ModelActionLogRepository

    def __init__(
            self,
            session: AsyncSession | async_scoped_session[AsyncSession],
            request: Request | None = None,
            **repo_kwargs: Any
    ):
        super().__init__(session, **repo_kwargs)
        self.request = request

    async def log(
            self,
            model: ModelT | dict[str, Any] | None,
            object_id: UUID | None,
            action: ActionType
    ):
        json = await self.request.json()
        user = self.request.user if self.request.scope.get("user") else None
        log = ModelActionLog(
            model_name=str(model.__class__.__name__),
            object_id=object_id,
            action=action,
            data=str(json),
            user=user,
        )
        await self.create(log)
