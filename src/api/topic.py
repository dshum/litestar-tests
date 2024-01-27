from uuid import UUID

from advanced_alchemy.filters import LimitOffset, OrderBy
from litestar import Controller, get, post, put, delete, Request
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from pydantic import TypeAdapter

from api.dependencies import provide_topic_service
from models.topic import TopicService, Topic
from schemas.topic import ListTopic, WriteTopicPayload, DetailedTopic


class TopicController(Controller):
    dependencies = {
        "topic_service": Provide(provide_topic_service),
    }

    @post(path="/topics")
    async def create_topic(
            self,
            topic_service: TopicService,
            data: WriteTopicPayload,
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
        return await topic_service.offset_pagination(topics, count, limit_offset, ListTopic)

    @get(path="/topics/{topic_id:uuid}")
    async def get_topic(
            self,
            topic_service: TopicService,
            topic_id: UUID = Parameter(
                title="Topic ID",
                description="The topic to retrieve",
            )) -> DetailedTopic:
        topic = await topic_service.get(topic_id)
        return DetailedTopic.model_validate(topic)

    @put(path="/topics/{topic_id:uuid}")
    async def update_topic(
            self,
            topic_service: TopicService,
            data: WriteTopicPayload,
            topic_id: UUID = Parameter(
                title="Topic ID",
                description="The topic to update",
            )
    ) -> DetailedTopic:
        data = data.model_dump()
        topic = await topic_service.update_and_log(Topic(**data), topic_id)
        return DetailedTopic.model_validate(topic)

    @delete(path="/topics/{topic_id:uuid}")
    async def delete_user(
            self,
            topic_service: TopicService,
            topic_id: UUID = Parameter(
                title="Topic ID",
                description="The topic to delete",
            ),
    ) -> None:
        await topic_service.delete(topic_id, auto_commit=True)
