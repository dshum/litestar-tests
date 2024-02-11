from datetime import timedelta, datetime
from typing import TYPE_CHECKING

from litestar.security.jwt import Token

from lib import settings
from lib.jwt_auth import jwt_auth

if TYPE_CHECKING:
    from models import User


class UserManager:
    @classmethod
    def encode_token(cls, user: "User") -> str:
        return jwt_auth.create_token(
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
