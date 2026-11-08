
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_email(subject, body, recipient):
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")

    if not email_address or not email_password:
        raise ValueError("Email credentials are missing.")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = email_address
    message["To"] = recipient
    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_address, email_password)
        server.send_message(message)

    print("Email notification sent successfully!")
