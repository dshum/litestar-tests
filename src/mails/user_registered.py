from typing import TYPE_CHECKING

from litestar.security.jwt import JWTAuth

from lib import settings
from lib.mail import Mailable
from lib.user_manager import UserManager

if TYPE_CHECKING:
    from models import User


class UserRegisteredMail(Mailable):
    def __init__(self, user: "User"):
        token = UserManager.encode_token(user)
        verify_url = f"{settings.app.FRONTEND_URL}/#/verify/{token}"

        super().__init__(
            subject="Welcome!",
            to=user.email,
            template_path="mails/user_registered.html",
            context={"user": user, "verify_url": verify_url},
        )
