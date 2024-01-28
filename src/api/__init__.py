from litestar import Router

from api.auth import AuthController
from api.topic import TopicController

site_router = Router(path="/", route_handlers=[
    AuthController,
    TopicController,
])
