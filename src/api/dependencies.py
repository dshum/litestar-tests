from typing import Literal

from advanced_alchemy.filters import SearchFilter
from litestar import Request
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset, OrderBy
from sqlalchemy.ext.asyncio import AsyncSession

from models.model_action_log import ModelActionLogService
from models.request_log import RequestLogService
from models.test import TestService
from models.topic import TopicService
from models.user import UserRepository, UserService


async def provide_limit_offset_pagination(
        offset: int = Parameter(query="offset", ge=0, default=0, required=False),
        limit: int = Parameter(query="limit", ge=1, default=10, required=False),
) -> LimitOffset:
    return LimitOffset(limit, offset)


async def provide_order_by(
        sort_by: str = Parameter(default="created_at", required=False),
        sort_order: Literal["asc", "desc"] = Parameter(default="desc", required=False),
) -> OrderBy:
    return OrderBy(field_name=sort_by, sort_order=sort_order)


async def provide_log_service(request: Request, db_session: AsyncSession) -> ModelActionLogService:
    return ModelActionLogService(session=db_session, request=request)


async def provide_request_log_service(request: Request, db_session: AsyncSession) -> RequestLogService:
    return RequestLogService(session=db_session, request=request)


async def provide_user_service(db_session: AsyncSession, log_service: ModelActionLogService) -> UserService:
    return UserService(session=db_session, log_service=log_service)


async def provide_topic_service(db_session: AsyncSession, log_service: ModelActionLogService) -> TopicService:
    return TopicService(session=db_session, log_service=log_service)


async def provide_test_service(db_session: AsyncSession, log_service: ModelActionLogService) -> TestService:
    return TestService(session=db_session, log_service=log_service)
