from email.message import EmailMessage
from typing import Any

import aiosmtplib

from lib import settings
from lib.template import environment


class Mailable:
    def __init__(
            self,
            to: list[str] | str,
            subject: str,
            template_path: str,
            context: dict[str, Any] | None = None,
            from_address: str | None = None,
    ):
        self.message = EmailMessage()
        self.message["From"] = from_address or settings.mail.FROM or settings.mail.USERNAME
        self.message["To"] = to
        self.message["Subject"] = subject

        template = environment.get_template(template_path)
        content = template.render(**context)
        self.message.set_content(content, subtype="html")

    async def send(self):
        print("Mailable.send", self.message["To"])

        return await aiosmtplib.send(
            self.message,
            hostname=settings.mail.HOST,
            port=settings.mail.PORT,
            username=settings.mail.USERNAME,
            password=settings.mail.PASSWORD,
            use_tls=settings.mail.USE_TLS,
            validate_certs=False,
            timeout=settings.mail.TIMEOUT,
        )
