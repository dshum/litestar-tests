from uuid import UUID

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from advanced_alchemy.filters import LimitOffset, OrderBy
from litestar import Controller, get, Request
from litestar.di import Provide
from litestar.dto import DTOConfig
from litestar.pagination import OffsetPagination
from litestar.params import Parameter

from api.dependencies import provide_test_service
from models.test import TestService, Test


class TestDTO(SQLAlchemyDTO[Test]):
    config = DTOConfig(exclude={"users", "questions", "updated_at",
                                "topic_id", "topic.created_at", "topic.updated_at"})


class TestController(Controller):
    path = "/tests"
    dependencies = {
        "test_service": Provide(provide_test_service),
    }
    return_dto = TestDTO

    @get(path="/")
    async def list_user_tests(
            self,
            request: Request,
            test_service: TestService,
            limit_offset: LimitOffset,
            order_by: OrderBy,
    ) -> OffsetPagination[Test]:
        tests, count = await test_service.get_user_tests(limit_offset, order_by, user_id=request.user.id)
        return await test_service.offset_pagination(tests, count, limit_offset)

    @get(path="/{test_id:uuid}")
    async def get_user_test(
            self,
            request: Request,
            test_service: TestService,
            test_id: UUID = Parameter(
                title="Test ID",
                description="The test to retrieve",
            )
    ) -> Test:
        return await test_service.get_user_test(id=test_id, user_id=request.user.id)
