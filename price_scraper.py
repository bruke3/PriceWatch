
import requests
from bs4 import BeautifulSoup


def get_product_price(url):
    response = requests.get(url, timeout=10)
    response.encoding = "utf-8"
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    price_element = soup.select_one(".price_color")

    if price_element is None:
        raise ValueError("Could not find product price.")

    price_text = price_element.get_text(strip=True)
    cleaned_price = price_text.replace("£", "").replace("Â", "").strip()

    try:
        return float(cleaned_price)
    except ValueError:
        raise ValueError(f"Invalid product price format: {price_text}")
