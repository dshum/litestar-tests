from datetime import timedelta, datetime
from typing import TYPE_CHECKING

from litestar.security.jwt import Token

from lib import settings

if TYPE_CHECKING:
    from models import User


class UserManager:
    @classmethod
    def encode_token(cls, user: "User") -> str:
        token = Token(
            sub=str(user.id),
            exp=datetime.now() + timedelta(minutes=settings.jwt.TTL),
            extras={"email": user.email},
        )
        return token.encode(secret=settings.jwt.SECRET, algorithm="HS256")

    @classmethod
    def decode_token(cls, token: str) -> Token:
        return Token.decode(token, settings.jwt.SECRET, "HS256")
