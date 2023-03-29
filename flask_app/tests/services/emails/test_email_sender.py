import pytest

from app.services.emails.email_sender import EmailSender
from tests.services.emails.conftest import Validations


@pytest.mark.parametrize(
    "subject, recipient",
    [
        ("E-mail address confirmation", "test@gmail.com"),
        ("Greeting email", "mock@gmail.com"),
    ]
)
def test__prepare_message(subject, recipient):
    message = EmailSender._prepare_message(subject, recipient)
    assert message['Subject'] == subject
    assert message['To'] == recipient
    assert message['From'] == EmailSender.email_address


def test_send_email(expected_message_plain, subject, recipient, plain_message,
                    mocked_email_address, mocked__send_email):
    EmailSender.send_email(plain_message, subject, recipient)
    passed_message = mocked__send_email.call_args.args[0]
    assert Validations.is_mimetext_content_equal(passed_message, expected_message_plain)


@pytest.mark.parametrize(
    "data",
    [
        ({'name': "John Doe"})
    ]
)
def test_send_email_html(expected_message_html, subject, recipient,
                         mocked_email_address, mocked__send_email,
                         test_resources_path, data):

    html_template_path = test_resources_path / 'email_body_template.html'
    EmailSender.send_email_html(html_template_path, data, subject, recipient)
    passed_message = mocked__send_email.call_args.args[0]
    assert Validations.is_mimetext_content_equal(passed_message, expected_message_html)

