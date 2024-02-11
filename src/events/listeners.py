from typing import TYPE_CHECKING

from litestar.events import listener

from mails.user_registered import UserRegisteredMail

if TYPE_CHECKING:
    from models import User


@listener("user_registered")
async def on_user_registered(user: "User", **kwargs) -> None:
    print("on_user_registered", user)
    await UserRegisteredMail(user=user).send()
