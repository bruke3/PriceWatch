
import json
from pathlib import Path
from urllib.parse import urlparse, urlunparse

DATA_FILE = Path(__file__).parent / "data" / "products.json"


def normalize_url(url):
    parsed = urlparse(url)

    return urlunparse((
        parsed.scheme.lower(),
        parsed.netloc.lower(),
        parsed.path.rstrip("/"),
        "",
        "",
        ""
    ))


def load_products():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            products = json.load(file)

    except json.JSONDecodeError:
        raise ValueError("The products file contains invalid JSON.")

    if not isinstance(products, list):
        raise ValueError("The products file must contain a list.")

    return products


def save_products(products):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    temp_file = DATA_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4)

    temp_file.replace(DATA_FILE)


def add_product():
    print("\n===== ADD PRODUCT =====")

    name = input("Product name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    url = input("Product URL: ").strip()
    parsed_url = urlparse(url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        print("Invalid product URL.")
        return

    products = load_products()
    normalized_url = normalize_url(url)

    for product in products:
        if normalize_url(product["url"]) == normalized_url:
            print("This product is already being tracked.")
            return

    try:
        target_price = float(input("Target price: "))

        if target_price <= 0:
            print("Target price must be greater than zero.")
            return

    except ValueError:
        print("Invalid price. Please enter a number.")
        return

    product = {
        "name": name,
        "url": url,
        "target_price": target_price,
        "alert_sent": False
    }

    products.append(product)
    save_products(products)

    print("\nProduct added successfully!")


def view_products():
    products = load_products()

    print("\n===== TRACKED PRODUCTS =====")

    if not products:
        print("No products are currently being tracked.")
        return

    for index, product in enumerate(products, start=1):
        print(f"\nProduct #{index}")
        print(f"Name: {product['name']}")
        print(f"URL: {product['url']}")
        print(f"Target Price: {product['target_price']:.2f}")
        print(f"Alert Sent: {product.get('alert_sent', False)}")
