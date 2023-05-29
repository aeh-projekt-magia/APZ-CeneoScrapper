import smtplib
import ssl
from pathlib import Path

from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.services.emails.email_exception import EmailException


class EmailSender:
    def __init__(
            self,
            port: int,
            smtp_server: str,
            email_address: str,
            password: str
    ):
        self.port = port
        self.smtp_server = smtp_server
        self.email_address = email_address
        self.password = password

    def send_email(self, message: str, subject: str, recipient: str):
        _message = self._prepare_message(subject, recipient)
        _message.attach(MIMEText(message, "plain"))
        self._send_email(_message)

    def send_email_html(self, template_path: Path, data: dict, subject: str, recipient: str):
        with template_path.open() as template:
            j2_template = Template(template.read(), keep_trailing_newline=True)
            message = j2_template.render(data)
        _message = self._prepare_message(subject, recipient)
        _message.attach(MIMEText(message, "html"))
        self._send_email(_message)

    def _prepare_message(self, subject: str, recipient: str) -> MIMEMultipart:
        _message = MIMEMultipart("alternative")
        _message["Subject"] = subject
        _message["From"] = self.email_address
        _message["To"] = recipient
        return _message

    def _send_email(self, message: MIMEMultipart):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.password)
                server.sendmail(
                    self.email_address, message["To"], message.as_string()
                )
        except smtplib.SMTPException as exception:
            print(exception)
            raise EmailException(f"Could not send the email to {message['To']}")
