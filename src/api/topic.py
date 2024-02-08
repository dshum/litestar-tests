from uuid import UUID

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from advanced_alchemy.filters import LimitOffset, OrderBy
from litestar import Controller, get
from litestar.di import Provide
from litestar.dto import DTOConfig
from litestar.pagination import OffsetPagination
from litestar.params import Parameter

from api.dependencies import provide_topic_service
from models.topic import TopicService, Topic


class TopicDTO(SQLAlchemyDTO[Topic]):
    config = DTOConfig(exclude={"updated_at", "tests"})


class TopicController(Controller):
    path = "/topics"
    dependencies = {
        "topic_service": Provide(provide_topic_service),
    }
    return_dto = TopicDTO

    @get(path="/")
    async def list_topics(
            self,
            topic_service: TopicService,
            limit_offset: LimitOffset,
            order_by: OrderBy,
    ) -> OffsetPagination[Topic]:
        topics, count = await topic_service.list_and_count(limit_offset, order_by)
        return await topic_service.offset_pagination(topics, count, limit_offset)

    @get(path="/{topic_id:uuid}")
    async def get_topic(
            self,
            topic_service: TopicService,
            topic_id: UUID = Parameter(
                title="Topic ID",
                description="The topic to retrieve",
            )
    ) -> Topic:
        return await topic_service.get(topic_id)
