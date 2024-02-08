from uuid import UUID

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from advanced_alchemy.filters import LimitOffset, OrderBy
from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.dto import DTOConfig
from litestar.pagination import OffsetPagination
from litestar.params import Parameter

from api.dependencies import provide_test_service
from models.test import TestService, Test
from schemas.test import WriteTestPayload


class TestDTO(SQLAlchemyDTO[Test]):
    config = DTOConfig(exclude={"users", "questions", "topic_id", "topic.created_at", "topic.updated_at"})


class TestController(Controller):
    path = "/tests"
    dependencies = {
        "test_service": Provide(provide_test_service),
    }
    return_dto = TestDTO

    @post(path="/")
    async def create_test(
            self,
            test_service: TestService,
            data: WriteTestPayload,
    ) -> Test:
        return await test_service.create(data.model_dump(), auto_commit=True)

    @get(path="/")
    async def list_tests(
            self,
            test_service: TestService,
            limit_offset: LimitOffset,
            order_by: OrderBy,
    ) -> OffsetPagination[Test]:
        tests, count = await test_service.list_and_count(limit_offset, order_by)
        return await test_service.offset_pagination(tests, count, limit_offset)

    @get(path="/{test_id:uuid}")
    async def get_test(
            self,
            test_service: TestService,
            test_id: UUID = Parameter(
                title="Test ID",
                description="The test to retrieve",
            )
    ) -> Test:
        return await test_service.get(test_id)

    @put(path="/{test_id:uuid}")
    async def update_test(
            self,
            test_service: TestService,
            data: WriteTestPayload,
            test_id: UUID = Parameter(
                title="Test ID",
                description="The test to update",
            )
    ) -> Test:
        data = data.model_dump()
        return await test_service.update(Test(**data), test_id)

    @delete(path="/{test_id:uuid}", return_dto=None)
    async def delete_user(
            self,
            test_service: TestService,
            test_id: UUID = Parameter(
                title="Test ID",
                description="The test to delete",
            ),
    ) -> None:
        await test_service.delete(test_id, auto_commit=True)
