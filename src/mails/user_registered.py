from typing import TYPE_CHECKING

from lib import settings
from lib.jwt import JWT
from lib.mail import Mailable

if TYPE_CHECKING:
    from models import User


class UserRegisteredMail(Mailable):
    def __init__(self, user: "User"):
        print("UserRegisteredMail.__init__", user)

        token = JWT.encode_token(user)
        verify_url = f"{settings.app.FRONTEND_URL}/#/verify/{token}"

        super().__init__(
            subject="Welcome!",
            to=user.email,
            template_path="mails/user_registered.html",
            context={"user": user, "verify_url": verify_url},
        )
