from uuid import UUID

from advanced_alchemy.filters import LimitOffset, OrderBy
from litestar import Controller, get, Request
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter

from api.dependencies import provide_test_service
from models.test import TestService
from schemas.test import ListTest, DetailedTest


class TestController(Controller):
    path = "/tests"
    dependencies = {
        "test_service": Provide(provide_test_service),
    }

    @get(path="/")
    async def list_user_tests(
            self,
            request: Request,
            test_service: TestService,
            limit_offset: LimitOffset,
            order_by: OrderBy,
    ) -> OffsetPagination[ListTest]:
        tests, count = await test_service.get_user_tests(limit_offset, order_by, user_id=request.user.id)
        data = await test_service.offset_pagination(tests, count, limit_offset, ListTest)
        return data

    @get(path="/{test_id:uuid}")
    async def get_user_test(
            self,
            request: Request,
            test_service: TestService,
            test_id: UUID = Parameter(
                title="Test ID",
                description="The test to retrieve",
            )) -> DetailedTest:
        test = await test_service.get_one(id=test_id, user=request.user)
        return DetailedTest.model_validate(test)
