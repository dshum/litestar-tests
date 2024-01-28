from litestar import Router

from api.admin.topic import TopicController
from api.admin.user import UserController
from middleware.guards.admin import admin_guard

admin_router = Router(
    path="/admin",
    route_handlers=[
        UserController,
        TopicController,
    ],
    guards=[admin_guard]
)
