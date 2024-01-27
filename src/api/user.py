from math import ceil
from typing import Any
from uuid import UUID

from litestar import Controller, get, post, patch, delete, put
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.pagination import ClassicPagination
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset, OrderBy
from pydantic import TypeAdapter

from api.dependencies import provide_user_repo, provide_user_service
from middleware.guards.admin import admin_guard
from models.user import UserRepository, User
from schemas.user import WriteUser, ReadUser
from services.user import UserService


class UserController(Controller):
    dependencies = {
        "user_service": Provide(provide_user_service),
        "user_repo": Provide(provide_user_repo),
    }
    guards = [admin_guard]

    @post(path="/users")
    async def create_user(
            self,
            user_service: UserService,
            data: WriteUser,
    ) -> ReadUser:
        return await user_service.create(data)

    @get(path="/users")
    async def list_users(
            self,
            user_service: UserService,
            limit_offset: LimitOffset,
            order_by: OrderBy,
    ) -> ClassicPagination[ReadUser]:
        return await user_service.list(limit_offset, order_by)

    @get(path="/users/{user_id:uuid}")
    async def get_user(
            self,
            user_service: UserService,
            user_id: UUID = Parameter(
                title="User ID",
                description="The user to retrieve.",
            ),
    ) -> ReadUser:
        return await user_service.get(user_id)

    @put(path="/users/{user_id:uuid}")
    async def update_user(
            self,
            user_service: UserService,
            data: WriteUser,
            user_id: UUID = Parameter(
                title="User ID",
                description="The user to update.",
            ),
    ) -> ReadUser:
        return await user_service.update(data, user_id)

    @delete(path="/users/{user_id:uuid}")
    async def delete_user(
            self,
            user_service: UserService,
            user_id: UUID = Parameter(
                title="User ID",
                description="The user to delete.",
            ),
    ) -> None:
        await user_service.delete(user_id)
