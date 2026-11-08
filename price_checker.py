
import requests
import smtplib

from price_scraper import get_product_price
from email_notifier import send_email
from product_manager import save_products


def check_prices(products):
    print("\n===== PRICE CHECK =====")

    if not products:
        print("No products to check.")
        return

    for product in products:
        print(f"\nChecking: {product['name']}")

        # Step 1: Get the current product price
        try:
            current_price = get_product_price(product["url"])

        except requests.exceptions.RequestException as error:
            print(f"Website connection error: {error}")
            continue

        except ValueError as error:
            print(f"Price extraction error: {error}")
            continue

        # Step 2: Compare current price with target price
        target_price = product["target_price"]

        print(f"Current price: £{current_price:.2f}")
        print(f"Target price: £{target_price:.2f}")

        if current_price <= target_price:
            print("Target reached! You can buy this product.")

            # Step 3: Send an email if an alert hasn't been sent
            if not product.get("alert_sent", False):

                try:
                    send_email(
                        subject=f"Price Alert: {product['name']}",
                        body=(
                            f"Good news!\n\n"
                            f"{product['name']} has reached your target price.\n"
                            f"Current price: £{current_price:.2f}\n"
                            f"Target price: £{target_price:.2f}\n\n"
                            f"Product link: {product['url']}"
                        ),
                        recipient="ethiopiauncovered3@gmail.com"
                    )

                    product["alert_sent"] = True

                except (smtplib.SMTPException, OSError, ValueError) as error:
                    print(f"Email delivery error: {error}")
                    continue

            else:
                print("Notification already sent. Skipping duplicate.")

        else:
            print("Price is still above your target.")
            product["alert_sent"] = False

    # Step 4: Save updated product information
    save_products(products)

