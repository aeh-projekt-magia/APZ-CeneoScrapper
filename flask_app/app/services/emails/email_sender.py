import smtplib
import ssl
from pathlib import Path

from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.services.emails.email_exception import EmailException
from config import Config


class EmailSender:
    port = 587  # tls port
    smtp_server = "smtp.gmail.com"
    email_address = Config.EMAIL_ADDRESS
    password = Config.EMAIL_PASSWORD

    @staticmethod
    def send_email(message: str, subject: str, recipient: str):
        _message = EmailSender._prepare_message(subject, recipient)
        _message.attach(MIMEText(message, "plain"))
        EmailSender._send_email(_message)

    @staticmethod
    def send_email_html(template_path: Path, data: dict, subject: str, recipient: str):
        with template_path.open() as template:
            j2_template = Template(template.read(), keep_trailing_newline=True)
            message = j2_template.render(data)
        _message = EmailSender._prepare_message(subject, recipient)
        _message.attach(MIMEText(message, "html"))
        EmailSender._send_email(_message)

    @staticmethod
    def _prepare_message(subject: str, recipient: str) -> MIMEMultipart:
        _message = MIMEMultipart("alternative")
        _message["Subject"] = subject
        _message["From"] = EmailSender.email_address
        _message["To"] = recipient
        return _message

    @staticmethod
    def _send_email(message: MIMEMultipart):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(EmailSender.smtp_server, EmailSender.port) as server:
                server.starttls(context=context)
                server.login(EmailSender.email_address, EmailSender.password)
                server.sendmail(EmailSender.email_address,
                                message["To"],
                                message.as_string())
        except smtplib.SMTPException as exception:
            # TODO: use logging
            print(exception)
            raise EmailException(f"Could not send the email to {message['To']}")
