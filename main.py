
from product_manager import add_product, view_products, load_products
from price_checker import check_prices


def show_menu():
    print("\n====== PRICEWATCH ======")
    print("1. Add Product")
    print("2. View Tracked Products")
    print("3. Check Prices")
    print("4. Exit")


def main():
    while True:
        show_menu()

        choice = input("\nSelect an option: ").strip()

        try:
            if choice == "1":
                add_product()

            elif choice == "2":
                view_products()

            elif choice == "3":
                check_prices(load_products())

            elif choice == "4":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()
