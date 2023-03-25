from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pytest

from flask_app.app.services.emails.email_sender import EmailSender


test_resources_path = Path(__file__).parent / "test_resources/"


@pytest.fixture
def subject():
    return "test subject"


@pytest.fixture
def recipient():
    return "recipient@gmail.com"


@pytest.fixture
def from_email_address():
    return 'testceneoscrapper@gmail.com'


@pytest.fixture
def mocked_email_address(mocker, from_email_address):
    mocker.patch(
        'flask_app.app.services.emails.email_sender.EmailSender.email_address',
        'testceneoscrapper@gmail.com'
    )


@pytest.fixture
def mocked_password(mocker):
    mocker.patch(
        'flask_app.app.services.emails.email_sender.EmailSender.password',
        'fake_password123'
    )


@pytest.fixture
def mocked__send_email(mocker):
    mock__send_email = mocker.stub(name="on__send_email_stub")
    mocker.patch(
        'flask_app.app.services.emails.email_sender.EmailSender._send_email',
        mock__send_email
    )
    return mock__send_email


@pytest.fixture
def plain_message():
    plain_message_path = test_resources_path / 'plain_message.txt'
    with plain_message_path.open() as html_template:
        message = html_template.read()
    return message


@pytest.fixture
def expected_message(subject, recipient, from_email_address):
    expected_message = MIMEMultipart("alternative")
    expected_message["Subject"] = subject
    expected_message["From"] = from_email_address
    expected_message["To"] = recipient
    return expected_message


@pytest.fixture
def expected_message_plain(expected_message, plain_message):
    expected_message.attach(MIMEText(plain_message, "plain"))
    return expected_message


@pytest.fixture
def expected_message_html(expected_message):
    html_expected_path = test_resources_path / 'email_body_expected.html'
    with html_expected_path.open() as html_template:
        message = html_template.read()
    expected_message.attach(MIMEText(message, "html"))
    return expected_message


@pytest.mark.parametrize(
    "subject, recipient",
    [
        ("E-mail address confirmation", "test@gmail.com")
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
    assert is_mimetext_content_equal(passed_message, expected_message_plain)


def test_send_email_html(expected_message_html, subject, recipient,
                         mocked_email_address, mocked__send_email):

    html_template_path = test_resources_path / 'email_body_template.html'
    data = {'name': "John Doe"}
    EmailSender.send_email_html(html_template_path, data, subject, recipient)
    passed_message = mocked__send_email.call_args.args[0]
    assert is_mimetext_content_equal(passed_message, expected_message_html)


def is_mimetext_content_equal(mime1: MIMEMultipart, mime2: MIMEMultipart):
    mime1_text = mime1.as_string().replace(mime1.get_boundary(), "")
    mime2_text = mime2.as_string().replace(mime2.get_boundary(), "")
    return mime1_text == mime2_text
