from collections.abc import Sequence
from typing import Any

from advanced_alchemy import ModelT
from advanced_alchemy.filters import LimitOffset
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService as _SQLAlchemyAsyncRepositoryService
from litestar.pagination import OffsetPagination
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from models.model_action_log import ModelActionLogService, ActionType


class SQLAlchemyAsyncRepositoryLoggedService(_SQLAlchemyAsyncRepositoryService[ModelT]):
    def __init__(
            self,
            session: AsyncSession | async_scoped_session[AsyncSession],
            log_service: ModelActionLogService | None = None,
            **repo_kwargs: Any
    ):
        super().__init__(session, **repo_kwargs)
        self.log_service = log_service

    @classmethod
    async def offset_pagination(
            cls,
            data: Sequence[ModelT],
            total: int,
            limit_offset: LimitOffset,
    ) -> OffsetPagination[ModelT]:
        return OffsetPagination[ModelT](
            items=data,
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    async def update(
            self,
            data: ModelT | dict[str, Any],
            item_id: Any | None = None,
            **kwargs: Any
    ) -> ModelT:
        await self.log_service.log(data, item_id, ActionType.UPDATE)
        return await super().update(data, item_id, **kwargs)

    async def delete(
            self,
            item_id: Any | None = None,
            **kwargs: Any
    ) -> ModelT:
        await self.log_service.log(None, item_id, ActionType.DELETE)
        return await super().delete(item_id, **kwargs)
