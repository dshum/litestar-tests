from email.message import EmailMessage
from typing import TYPE_CHECKING, Tuple, Dict

import aiosmtplib
from aiosmtplib import SMTPResponse

from lib import settings
from lib.template import environment

if TYPE_CHECKING:
    from models import User


async def send_user_registered_email(user: "User") -> tuple[dict[str, SMTPResponse], str]:
    message = EmailMessage()
    message["From"] = settings.mail.USERNAME
    message["To"] = user.email
    message["Subject"] = "Welcome!"

    template = environment.get_template("mails/user_registered.html")
    content = template.render(user=user)
    message.set_content(content, subtype="html")

    return await aiosmtplib.send(
        message,
        hostname=settings.mail.HOST,
        port=settings.mail.PORT,
        username=settings.mail.USERNAME,
        password=settings.mail.PASSWORD,
        use_tls=True,
        timeout=10,
    )
