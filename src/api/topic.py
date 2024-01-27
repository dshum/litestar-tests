from uuid import UUID

from advanced_alchemy.filters import LimitOffset, OrderBy
from litestar import Controller, get, post
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from pydantic import TypeAdapter

from api.dependencies import provide_topic_service
from models.topic import TopicService
from schemas.topic import ListTopic, WriteTopic, DetailedTopic


class TopicController(Controller):
    dependencies = {
        "topic_service": Provide(provide_topic_service),
    }

    @post(path="/topics")
    async def create_topic(
            self,
            topic_service: TopicService,
            data: WriteTopic,
    ) -> DetailedTopic:
        new_topic = await topic_service.create(data.model_dump(), auto_commit=True)
        return DetailedTopic.model_validate(new_topic)

    @get(path="/topics")
    async def list_topics(
            self,
            topic_service: TopicService,
            limit_offset: LimitOffset,
            order_by: OrderBy,
    ) -> OffsetPagination[ListTopic]:
        topics, count = await topic_service.list_and_count(limit_offset, order_by)
        type_adapter = TypeAdapter(list[ListTopic])
        return OffsetPagination[ListTopic](
            items=type_adapter.validate_python(topics),
            total=count,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @get(path="/topics/{topic_id:uuid}")
    async def get_topic(
            self,
            topic_service: TopicService,
            topic_id: UUID = Parameter(
                title="Topic ID",
                description="The topic to retrieve.",
            )) -> DetailedTopic:
        topic = await topic_service.get(topic_id)
        return DetailedTopic.model_validate(topic)
