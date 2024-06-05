from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from jinja2 import Environment, select_autoescape, PackageLoader


from ..core.config import settings


env = Environment(
    loader=PackageLoader("app", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Email:
    def __init__(self, user: str, token: str, email: List[EmailSchema]):
        """
        Initialize the class with user information, authentication token, and a list of email schemas.

        Parameters:
            user (str): The user's information.
            token (str): The authentication token.
            email (List[EmailSchema]): A list of email schemas.

        Returns:
            None
        """
        self.email = email
        self.token = token
        self.name = user
        self.sender = "Revas <admin@revas.com>"

    async def sendMail(self, subject, template):
        """
        Asynchronously sends an email using the specified subject and template.

        :param subject: The subject of the email.
        :param template: The template to use for the email.
        :return: None
        """
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )

        template = env.get_template(f"{template}.html")
        html = template.render(token=self.token, name=self.name, subject=subject)

        message = MessageSchema(
            subject=subject, recipients=self.email, body=html, subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message)

    async def sendVerificationEmail(self):
        """
        Asynchronously sends a verification email using the sendMail method with the subject "Verify your Account" and the template "verification".
        """
        await self.sendMail("Verify your Account", "verification")
