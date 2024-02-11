from datetime import timedelta
from typing import Any, Optional, TYPE_CHECKING

from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTAuth, Token

from lib import settings
from lib.database import async_sessionmaker
from models import User


async def retrieve_user_handler(
        token: Token,
        connection: ASGIConnection[Any, Any, Any, Any],
) -> Optional["User"]:
    db_engine = connection.app.state.db_engine
    async with async_sessionmaker(bind=db_engine) as session:
        user = await session.get(User, token.sub)
    return user


jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.jwt.SECRET,
    default_token_expiration=timedelta(minutes=settings.jwt.TTL),
    exclude=["/register", "/login", "/verify", "/schema"],
)


class JWT:
    @classmethod
    async def encode_token(cls, user: User) -> str:
        return await jwt_auth.create_token(
            identifier=user.id,
            token_extras={"email": user.email}
        )

    @classmethod
    def decode_token(cls, token: str) -> Token:
        return Token.decode(
            encoded_token=token,
            secret=jwt_auth.token_secret,
            algorithm=jwt_auth.algorithm,
        )
