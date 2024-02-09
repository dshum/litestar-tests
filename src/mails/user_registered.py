from typing import TYPE_CHECKING

from lib.mail import Mailable

if TYPE_CHECKING:
    from models import User


class UserRegisteredMail(Mailable):
    def __init__(self, user: "User"):
        super().__init__(
            subject="Welcome!",
            to=user.email,
            template_path="mails/user_registered.html",
            context={"user": user}
        )
