from typing import TYPE_CHECKING

from litestar.events import listener

from lib.jwt import JWT
from mails.password_reset import PasswordResetMail
from mails.user_registered import UserRegisteredMail

if TYPE_CHECKING:
    from models import User, PasswordReset


@listener("user_registered")
async def on_user_registered(user: "User", **kwargs) -> None:
    token = JWT.encode_token(user)
    await UserRegisteredMail(user=user, token=token).send()


@listener("password_reset")
async def on_password_reset(user: "User", token: str, **kwargs) -> None:
    await PasswordResetMail(user=user, token=token).send()
