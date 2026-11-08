
import smtplib
from unittest.mock import Mock, patch

import pytest

from email_notifier import send_email


def test_email_is_sent_successfully(monkeypatch):
    monkeypatch.setenv("EMAIL_ADDRESS", "sender@gmail.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "test_password")

    mock_server = Mock()

    with patch(
        "email_notifier.smtplib.SMTP_SSL"
    ) as mock_smtp:

        mock_smtp.return_value.__enter__.return_value = mock_server

        send_email(
            subject="Price Alert",
            body="The product has reached your target price.",
            recipient="receiver@gmail.com"
        )

    mock_server.login.assert_called_once_with(
        "sender@gmail.com",
        "test_password"
    )

    mock_server.send_message.assert_called_once()

    message = mock_server.send_message.call_args[0][0]

    assert message["Subject"] == "Price Alert"
    assert message["To"] == "receiver@gmail.com"
    assert "reached your target price" in message.get_content()


def test_missing_email_credentials_raises_error(monkeypatch):
    monkeypatch.delenv("EMAIL_ADDRESS", raising=False)
    monkeypatch.delenv("EMAIL_PASSWORD", raising=False)

    with pytest.raises(ValueError, match="Email credentials are missing"):
        send_email(
            "Price Alert",
            "Test message",
            "receiver@gmail.com"
        )


def test_email_delivery_failure_raises_error(monkeypatch):
    monkeypatch.setenv("EMAIL_ADDRESS", "sender@gmail.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "test_password")

    with patch(
        "email_notifier.smtplib.SMTP_SSL",
        side_effect=smtplib.SMTPException("Connection failed")
    ):
        with pytest.raises(smtplib.SMTPException):
            send_email(
                "Price Alert",
                "Test message",
                "receiver@gmail.com"
            )
