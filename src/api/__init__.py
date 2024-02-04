from litestar import Router

from api.auth import AuthController
from api.test import TestController
from api.topic import TopicController

site_router = Router(path="/", route_handlers=[
    AuthController,
    TopicController,
    TestController,
])
