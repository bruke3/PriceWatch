
import smtplib
import requests
from unittest.mock import patch

from price_checker import check_prices


def test_email_sent_when_target_reached():
    products = [
        {
            "name": "Gaming Mouse",
            "url": "https://example.com/mouse",
            "target_price": 50,
            "alert_sent": False
        }
    ]

    with patch("price_checker.get_product_price", return_value=40):
        with patch("price_checker.send_email") as mock_email:
            with patch("price_checker.save_products"):
                check_prices(products)

    mock_email.assert_called_once()


def test_no_email_when_price_is_above_target():
    products = [
        {
            "name": "Gaming Mouse",
            "url": "https://example.com/mouse",
            "target_price": 50,
            "alert_sent": False
        }
    ]

    with patch("price_checker.get_product_price", return_value=60):
        with patch("price_checker.send_email") as mock_email:
            with patch("price_checker.save_products"):
                check_prices(products)

    mock_email.assert_not_called()


def test_no_duplicate_email():
    products = [
        {
            "name": "Gaming Mouse",
            "url": "https://example.com/mouse",
            "target_price": 50,
            "alert_sent": True
        }
    ]

    with patch("price_checker.get_product_price", return_value=40):
        with patch("price_checker.send_email") as mock_email:
            with patch("price_checker.save_products"):
                check_prices(products)

    mock_email.assert_not_called()


def test_alert_resets_when_price_rises():
    products = [
        {
            "name": "Gaming Mouse",
            "url": "https://example.com/mouse",
            "target_price": 50,
            "alert_sent": True
        }
    ]

    with patch("price_checker.get_product_price", return_value=60):
        with patch("price_checker.send_email"):
            with patch("price_checker.save_products"):
                check_prices(products)

    assert products[0]["alert_sent"] is False


def test_scraper_failure_does_not_stop_other_products():
    products = [
        {
            "name": "Product A",
            "url": "https://example.com/a",
            "target_price": 50,
            "alert_sent": False
        },
        {
            "name": "Product B",
            "url": "https://example.com/b",
            "target_price": 50,
            "alert_sent": False
        }
    ]

    with patch(
        "price_checker.get_product_price",
        side_effect=[
            requests.exceptions.RequestException("Network error"),
            40
        ]
    ):
        with patch("price_checker.send_email") as mock_email:
            with patch("price_checker.save_products"):
                check_prices(products)

    mock_email.assert_called_once()
    assert products[1]["alert_sent"] is True


def test_email_failure_does_not_mark_alert_as_sent():
    products = [
        {
            "name": "Gaming Mouse",
            "url": "https://example.com/mouse",
            "target_price": 50,
            "alert_sent": False
        }
    ]

    with patch("price_checker.get_product_price", return_value=40):
        with patch(
            "price_checker.send_email",
            side_effect=smtplib.SMTPException("Email sending failed")
        ):
            with patch("price_checker.save_products"):
                check_prices(products)

    assert products[0]["alert_sent"] is False

