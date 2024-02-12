from typing import TYPE_CHECKING

from litestar.events import listener

from mails.user_registered import UserRegisteredMail

if TYPE_CHECKING:
    from models import User


@listener("user_registered")
async def on_user_registered(user: "User", **kwargs) -> None:
    await UserRegisteredMail(user=user).send()


@listener("password_reset")
async def on_password_reset(user: "User", **kwargs) -> None:
    await PasswordResetMail(user=user).send()
