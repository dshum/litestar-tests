from datetime import timedelta
from typing import Any, Optional

from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTAuth, Token

from lib import settings
from lib.database import async_sessionmaker
from models.user import User


async def retrieve_user_handler(
        token: Token,
        connection: ASGIConnection[Any, Any, Any, Any],
) -> Optional[User]:
    db_engine = connection.app.state.db_engine
    async with async_sessionmaker(bind=db_engine) as session:
        user = await session.get(User, token.sub)
    return user


jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.jwt.SECRET,
    default_token_expiration=timedelta(minutes=settings.jwt.TTL),
    exclude=["/login", "/schema"],
)
