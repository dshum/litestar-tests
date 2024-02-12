from lib import settings
from lib.mail import Mailable


class PasswordResetMail(Mailable):
    def __init__(self, user: "User"):
        print("UserRegisteredMail.__init__", user)

        password_reset_url = f"{settings.app.FRONTEND_URL}/#/verify/{token}"

        super().__init__(
            subject="Welcome!",
            to=user.email,
            template_path="mails/password_reset.html",
            context={"user": user, "password_reset_url": password_reset_url},
        )
