from uuid import UUID

from advanced_alchemy.filters import LimitOffset, OrderBy
from litestar import Controller, get, post, put, delete, Request
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from pydantic import TypeAdapter

from api.dependencies import provide_test_service
from models.test import TestService, Test
from schemas.test import ListTest, WriteTestPayload, DetailedTest


class TestController(Controller):
    path = "/tests"
    dependencies = {
        "test_service": Provide(provide_test_service),
    }

    @post(path="/")
    async def create_test(
            self,
            test_service: TestService,
            data: WriteTestPayload,
    ) -> DetailedTest:
        new_test = await test_service.create(data.model_dump(), auto_commit=True)
        return DetailedTest.model_validate(new_test)

    @get(path="/")
    async def list_tests(
            self,
            test_service: TestService,
            limit_offset: LimitOffset,
            order_by: OrderBy,
    ) -> OffsetPagination[ListTest]:
        tests, count = await test_service.list_and_count(limit_offset, order_by)
        return await test_service.offset_pagination(tests, count, limit_offset, ListTest)

    @get(path="/{test_id:uuid}")
    async def get_test(
            self,
            test_service: TestService,
            test_id: UUID = Parameter(
                title="Test ID",
                description="The test to retrieve",
            )) -> DetailedTest:
        test = await test_service.get(test_id)
        return DetailedTest.model_validate(test)

    @put(path="/{test_id:uuid}")
    async def update_test(
            self,
            test_service: TestService,
            data: WriteTestPayload,
            test_id: UUID = Parameter(
                title="Test ID",
                description="The test to update",
            )
    ) -> DetailedTest:
        data = data.model_dump()
        test = await test_service.update(Test(**data), test_id)
        return DetailedTest.model_validate(test)

    @delete(path="/{test_id:uuid}")
    async def delete_user(
            self,
            test_service: TestService,
            test_id: UUID = Parameter(
                title="Test ID",
                description="The test to delete",
            ),
    ) -> None:
        await test_service.delete(test_id, auto_commit=True)
