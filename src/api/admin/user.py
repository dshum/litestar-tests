from uuid import UUID

from advanced_alchemy.filters import LimitOffset, OrderBy
from litestar import Controller, get, post, put, delete, Request
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from pydantic import TypeAdapter

from api.dependencies import provide_user_service, provide_user_service
from models.user import UserService, User
from schemas.user import ListUser, DetailedUser, WriteUserPayload


class UserController(Controller):
    path = "/users"
    dependencies = {
        "user_service": Provide(provide_user_service),
    }

    @post(path="/")
    async def create_user(
            self,
            user_service: UserService,
            data: WriteUserPayload,
    ) -> DetailedUser:
        new_user = await user_service.create(data.model_dump(), auto_commit=True)
        return DetailedUser.model_validate(new_user)

    @get(path="/")
    async def list_users(
            self,
            user_service: UserService,
            limit_offset: LimitOffset,
            order_by: OrderBy,
    ) -> OffsetPagination[ListUser]:
        users, count = await user_service.list_and_count(limit_offset, order_by)
        return await user_service.offset_pagination(users, count, limit_offset, ListUser)

    @get(path="/{user_id:uuid}")
    async def get_user(
            self,
            user_service: UserService,
            user_id: UUID = Parameter(
                title="User ID",
                description="The user to retrieve",
            )) -> DetailedUser:
        user = await user_service.get(user_id)
        return DetailedUser.model_validate(user)

    @put(path="/{user_id:uuid}")
    async def update_user(
            self,
            user_service: UserService,
            data: WriteUserPayload,
            user_id: UUID = Parameter(
                title="User ID",
                description="The user to update",
            )
    ) -> DetailedUser:
        data = data.model_dump()
        user = await user_service.update(User(**data), user_id, auto_commit=True)
        return DetailedUser.model_validate(user)

    @delete(path="/{user_id:uuid}")
    async def delete_user(
            self,
            user_service: UserService,
            user_id: UUID = Parameter(
                title="User ID",
                description="The user to delete",
            ),
    ) -> None:
        await user_service.delete(user_id, auto_commit=True)
