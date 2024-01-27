from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers import BaseRouteHandler

from models.user import UserRole


def admin_guard(connection: ASGIConnection, route_handler: BaseRouteHandler) -> None:
    if connection.user.role != UserRole.ADMIN:
        raise NotAuthorizedException("Only admins allowed managing users")
