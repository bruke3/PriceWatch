
from unittest.mock import Mock, patch

import pytest
import requests

from price_scraper import get_product_price


def test_extracts_product_price():
    html = """
    <html>
        <p class="price_color">£51.77</p>
    </html>
    """

    mock_response = Mock()
    mock_response.text = html

    with patch("price_scraper.requests.get", return_value=mock_response):
        price = get_product_price("https://example.com/book")

    assert price == 51.77


def test_missing_price_element_raises_error():
    html = """
    <html>
        <p>No price available</p>
    </html>
    """

    mock_response = Mock()
    mock_response.text = html

    with patch("price_scraper.requests.get", return_value=mock_response):
        with pytest.raises(ValueError, match="Could not find product price"):
            get_product_price("https://example.com/book")


def test_invalid_price_format_raises_error():
    html = """
    <html>
        <p class="price_color">Invalid Price</p>
    </html>
    """

    mock_response = Mock()
    mock_response.text = html

    with patch("price_scraper.requests.get", return_value=mock_response):
        with pytest.raises(ValueError):
            get_product_price("https://example.com/book")


def test_website_connection_failure():
    with patch(
        "price_scraper.requests.get",
        side_effect=requests.exceptions.RequestException("Connection failed")
    ):
        with pytest.raises(requests.exceptions.RequestException):
            get_product_price("https://example.com/book")
