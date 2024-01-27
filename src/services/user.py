from math import ceil
from uuid import UUID

from litestar.pagination import ClassicPagination
from litestar.repository.filters import LimitOffset, OrderBy
from pydantic import TypeAdapter

from models.user import UserRepository, User
from schemas.user import ReadUser, WriteUser


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def list(self, limit_offset: LimitOffset, order_by: OrderBy):
        results, total = await self.repository.list_and_count(limit_offset, order_by)
        type_adapter = TypeAdapter(list[ReadUser])
        return ClassicPagination[ReadUser](
            items=type_adapter.validate_python(results),
            total_pages=ceil(total / limit_offset.limit),
            page_size=limit_offset.limit,
            current_page=limit_offset.offset + 1,
        )

    async def create(self, data: WriteUser) -> ReadUser:
        obj = await self.repository.add(
            User(**data.model_dump(exclude_unset=True, exclude_none=True)),
        )
        await self.repository.session.commit()
        return ReadUser.model_validate(obj)

    async def get(self, user_id: UUID) -> ReadUser:
        obj = await self.repository.get(user_id)
        return ReadUser.model_validate(obj)

    async def update(self, data: WriteUser, user_id: UUID) -> ReadUser:
        data = data.model_dump()
        data.update({"id": user_id})
        obj = await self.repository.update(User(**data))
        await self.repository.session.commit()
        return ReadUser.model_validate(obj)

    async def delete(self, user_id: UUID) -> None:
        _ = await self.repository.delete(user_id)
        await self.repository.session.commit()
