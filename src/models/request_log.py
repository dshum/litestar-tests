from enum import Enum
from enum import Enum
from typing import Any, TYPE_CHECKING
from uuid import UUID

from advanced_alchemy import SQLAlchemyAsyncRepository, SQLAlchemyAsyncRepositoryService
from advanced_alchemy.base import UUIDAuditBase
from litestar import Request, Response
from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import User


class Method(str, Enum):
    GET = "Get"
    POST = "Post"
    PUT = "Put"
    PATCH = "Patch"
    DELETE = "Delete"


class RequestLog(UUIDAuditBase):
    __tablename__ = "request_logs"

    method: Mapped[Method]
    url: Mapped[str]
    headers: Mapped[dict[str: Any] | None] = mapped_column(JSONB, default=None)
    body: Mapped[dict[str: Any] | None] = mapped_column(JSONB, default=None)
    user_agent: Mapped[str] = mapped_column(Text, default=None)
    ip_address: Mapped[str] = mapped_column(Text, default=None)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="restrict"), default=None)
    user: Mapped["User"] = relationship(
        foreign_keys="RequestLog.user_id",
        lazy="immediate",
    )
    status_code: Mapped[int]
    response_headers: Mapped[dict[str: Any] | None] = mapped_column(JSONB, default=None)
    response: Mapped[dict[str: Any] | None] = mapped_column(JSONB, default=None)


class RequestLogRepository(SQLAlchemyAsyncRepository[RequestLog]):
    model_type = RequestLog


class RequestLogService(SQLAlchemyAsyncRepositoryService[RequestLog]):
    repository_type = RequestLogRepository

    def __init__(
            self,
            session: AsyncSession | async_scoped_session[AsyncSession],
            request: Request | None = None,
            response: Response | None = None,
            **repo_kwargs: Any
    ):
        super().__init__(session, **repo_kwargs)
        self.request = request
        self.response = response

    async def log(self):
        body = await self.request.json()

        # print(self.request.scope.items())

        log = RequestLog(
            method=self.request.method,
            url=self.request.url.path,
            headers=self.request.headers.dict(),
            body=body,
            user=self.request.user,
            user_agent=self.request.headers.get("user-agent"),
            ip_address=str(self.request.client.host),
            status_code=200,
            response=None,
            response_headers={}
        )
        await self.create(log, auto_commit=True)
