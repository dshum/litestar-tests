from uuid import UUID

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from advanced_alchemy.filters import LimitOffset, OrderBy
from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.dto import DTOConfig
from litestar.pagination import OffsetPagination
from litestar.params import Parameter

from api.dependencies import provide_user_service
from models.user import UserService, User
from schemas.user import WriteUserPayload


class UserDTO(SQLAlchemyDTO[User]):
    config = DTOConfig(exclude={"password", "updated_at", "tests", "assigned_tests"})


class UserController(Controller):
    path = "/users"
    dependencies = {
        "user_service": Provide(provide_user_service),
    }
    return_dto = UserDTO

    @post(path="/")
    async def create_user(
            self,
            user_service: UserService,
            data: WriteUserPayload,
    ) -> User:
        return await user_service.create(data.model_dump(), auto_commit=True)

    @get(path="/")
    async def list_users(
            self,
            user_service: UserService,
            limit_offset: LimitOffset,
            order_by: OrderBy,
    ) -> OffsetPagination[User]:
        users, count = await user_service.list_and_count(limit_offset, order_by)
        return await user_service.offset_pagination(users, count, limit_offset)

    @get(path="/{user_id:uuid}")
    async def get_user(
            self,
            user_service: UserService,
            user_id: UUID = Parameter(
                title="User ID",
                description="The user to retrieve",
            )
    ) -> User:
        return await user_service.get(user_id)

    @put(path="/{user_id:uuid}")
    async def update_user(
            self,
            user_service: UserService,
            data: WriteUserPayload,
            user_id: UUID = Parameter(
                title="User ID",
                description="The user to update",
            )
    ) -> User:
        data = data.model_dump()
        return await user_service.update(User(**data), user_id, auto_commit=True)

    @delete(path="/{user_id:uuid}", return_dto=None)
    async def delete_user(
            self,
            user_service: UserService,
            user_id: UUID = Parameter(
                title="User ID",
                description="The user to delete",
            ),
    ) -> None:
        await user_service.delete(user_id, auto_commit=True)
