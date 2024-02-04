from litestar import Router

from api.admin.test import TestController
from api.admin.topic import TopicController
from api.admin.user import UserController
from middleware.guards.admin import admin_guard

admin_router = Router(
    path="/admin",
    route_handlers=[
        UserController,
        TopicController,
        TestController,
    ],
    guards=[admin_guard]
)
