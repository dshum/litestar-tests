from advanced_alchemy import NotFoundError, ConflictError
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin
from litestar.di import Provide
from litestar.exceptions import ValidationException, NotAuthorizedException, HTTPException, NotFoundException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

from api.auth import AuthController
from api.dependencies import provide_limit_offset_pagination, provide_order_by
from api.topic import TopicController
from api.user import UserController
from lib import sentry, database, settings
from lib.database import db_config
from lib.exceptions import (
    app_exception_handler,
    default_exception_handler,
    not_found_exception_handler,
    conflict_exception_handler,
)
from lib.jwt_auth import jwt_auth
from lib.logs import logging_config

app = Litestar(
    route_handlers=[AuthController, UserController, TopicController],
    plugins=[
        SQLAlchemyPlugin(db_config),
    ],
    on_startup=[sentry.on_startup, database.on_startup],
    on_app_init=[jwt_auth.on_app_init],
    dependencies={
        "limit_offset": Provide(provide_limit_offset_pagination),
        "order_by": Provide(provide_order_by)
    },
    exception_handlers={
        ValidationException: default_exception_handler,
        NotAuthorizedException: default_exception_handler,
        NotFoundException: not_found_exception_handler,
        NotFoundError: not_found_exception_handler,
        ConflictError: conflict_exception_handler,
        ValueError: default_exception_handler,
        HTTP_500_INTERNAL_SERVER_ERROR: app_exception_handler,
        HTTPException: app_exception_handler,
    },
    logging_config=logging_config,
    debug=settings.app.DEBUG,
)