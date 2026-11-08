# PriceWatch

A Python command-line application that tracks product prices and sends email notifications when products reach your target prices.

## Features

- Add products using their names, URLs, and target prices.
- View all tracked products.
- Extract product prices from supported websites.
- Compare current prices against target prices.
- Send email notifications when target prices are reached.
- Prevent duplicate email notifications.
- Store product information in JSON.
- Handle website, price extraction, and email delivery errors.
- Automated tests using pytest.

## Technologies Used

- Python
- Requests
- Beautiful Soup 4
- JSON
- SMTP / Gmail
- Python-dotenv
- Pytest

## Project Structure


PriceWatch/
├── data/
│   └── products.json
├── tests/
│   ├── test_email_notifier.py
│   ├── test_price_checker.py
│   ├── test_price_scraper.py
│   └── test_product_manager.py
├── main.py
├── product_manager.py
├── price_scraper.py
├── price_checker.py
├── email_notifier.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md


## Installation

1. Clone the repository:


git clone https://github.com/bruke3/PriceWatch.git


2. Navigate into the project directory:


cd PriceWatch


3. Create a virtual environment:


python -m venv .venv


4. Activate the virtual environment.

Windows PowerShell:


.\.venv\Scripts\Activate.ps1


5. Install dependencies:


pip install -r requirements.txt


## Email Configuration

Create a `.env` file in the project root:


EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password


Use a Gmail App Password rather than your regular Gmail password.

Never share or upload your `.env` file.

## Running the Application

Start PriceWatch:


python main.py


Use the menu to:

1. Add a product.
2. View tracked products.
3. Check product prices.
4. Exit the application.

## Running Tests

Run the complete test suite:


python -m pytest -v


The tests use mocks to simulate website responses and email delivery, so they do not require real website requests or email messages.

## Current Limitations

- Price extraction currently relies on the `.price_color` HTML selector, so websites with different page structures require scraper adjustments.
- Price checks are initiated manually through the command-line menu.
- Prices and notifications currently use GBP formatting.

## Future Improvements

- Support more e-commerce websites.
- Add price history tracking.
- Introduce automatic scheduled price checks.
- Improve currency handling.
- Build a graphical or web-based interface.

## Author

Developed as a Python portfolio project to practice web scraping, application development, data storage, error handling, email automation, and software testing.
