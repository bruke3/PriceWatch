
import json
from unittest.mock import patch

import pytest

import product_manager


def test_missing_file_returns_empty_list(tmp_path, monkeypatch):
    file_path = tmp_path / "products.json"
    monkeypatch.setattr(product_manager, "DATA_FILE", file_path)

    products = product_manager.load_products()

    assert products == []


def test_corrupted_json_raises_error(tmp_path, monkeypatch):
    file_path = tmp_path / "products.json"
    file_path.write_text("{invalid json", encoding="utf-8")

    monkeypatch.setattr(product_manager, "DATA_FILE", file_path)

    with pytest.raises(ValueError, match="invalid JSON"):
        product_manager.load_products()


def test_save_and_load_products(tmp_path, monkeypatch):
    file_path = tmp_path / "products.json"
    monkeypatch.setattr(product_manager, "DATA_FILE", file_path)

    products = [
        {
            "name": "Gaming Mouse",
            "url": "https://example.com/mouse",
            "target_price": 50,
            "alert_sent": False
        }
    ]

    product_manager.save_products(products)
    loaded_products = product_manager.load_products()

    assert loaded_products == products


def test_duplicate_url_with_tracking_parameter_is_rejected(
    tmp_path, monkeypatch, capsys
):
    file_path = tmp_path / "products.json"
    monkeypatch.setattr(product_manager, "DATA_FILE", file_path)

    products = [
        {
            "name": "Book",
            "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
            "target_price": 60,
            "alert_sent": False
        }
    ]

    product_manager.save_products(products)

    user_inputs = [
        "Another Book",
        "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html?utm_source=chatgpt.com"
    ]

    with patch("builtins.input", side_effect=user_inputs):
        product_manager.add_product()

    output = capsys.readouterr().out

    assert "already being tracked" in output

    saved_products = product_manager.load_products()
    assert len(saved_products) == 1


def test_new_product_is_added_successfully(tmp_path, monkeypatch):
    file_path = tmp_path / "products.json"
    monkeypatch.setattr(product_manager, "DATA_FILE", file_path)

    user_inputs = [
        "Gaming Mouse",
        "https://example.com/mouse",
        "50"
    ]

    with patch("builtins.input", side_effect=user_inputs):
        product_manager.add_product()

    products = product_manager.load_products()

    assert len(products) == 1
    assert products[0]["name"] == "Gaming Mouse"
    assert products[0]["target_price"] == 50
    assert products[0]["alert_sent"] is False
