from typing import TYPE_CHECKING

from lib import settings
from lib.mail import Mailable

if TYPE_CHECKING:
    from models import User


class VerifyEmailMail(Mailable):
    def __init__(self, user: "User", token: str):
        verify_url = f"{settings.app.FRONTEND_URL}/#/verify/{token}"
        super().__init__(
            subject="Email verification",
            to=user.email,
            template_path="mails/verify_email.html",
            context={"user": user, "verify_url": verify_url},
        )
