from collections.abc import AsyncGenerator
from typing import Literal

from litestar.exceptions import ClientException
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset, OrderBy
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.topic import TopicService
from models.user import UserRepository, User
from services.auth import AuthService
from services.user import UserService


async def provide_limit_offset_pagination(
        current_page: int = Parameter(ge=1, query="page", default=1, required=False),
        page_size: int = Parameter(
            query="pageSize",
            ge=1,
            default=10,
            required=False,
        ),
) -> LimitOffset:
    """Add offset/limit pagination.

    Return type consumed by `Repository.apply_limit_offset_pagination()`.

    Parameters
    ----------
    current_page : int
        LIMIT to apply to select.
    page_size : int
        OFFSET to apply to select.
    """
    return LimitOffset(page_size, page_size * (current_page - 1))


async def provide_order_by(
        sort_by: str = Parameter(default="created_at", required=False),
        sort_order: Literal["asc", "desc"] = Parameter(default="desc", required=False),
) -> OrderBy:
    return OrderBy(field_name=sort_by, sort_order=sort_order)


async def provide_auth_service(user_repo: UserRepository) -> AuthService:
    return AuthService(repository=user_repo)


async def provide_user_service(user_repo: UserRepository) -> UserService:
    return UserService(repository=user_repo)


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(
        statement=select(User),
        session=db_session,
    )


async def provide_user_details_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(
        statement=select(User),
        session=db_session,
    )


async def provide_login_user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(
        statement=select(User),
        session=db_session,
    )


async def provide_topic_service(db_session: AsyncSession) -> TopicService:
    return TopicService(session=db_session)
