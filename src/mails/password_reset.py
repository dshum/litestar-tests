from typing import TYPE_CHECKING

from lib import settings
from lib.mail import Mailable

if TYPE_CHECKING:
    from models import User, PasswordReset


class PasswordResetMail(Mailable):
    def __init__(self, user: "User", token: str):
        password_reset_url = f"{settings.app.FRONTEND_URL}/#/password-reset/{token}"

        super().__init__(
            subject="Password reset",
            to=user.email,
            template_path="mails/password_reset.html",
            context={"user": user, "password_reset_url": password_reset_url},
        )
