from twilio.rest import Client
import smtplib
import os

TWILIO_SID = os.environ["twilio_sid"]
TWILIO_AUTH_TOKEN = os.environ["twilio_auth"]
TWILIO_VIRTUAL_NUMBER = os.environ["twilio_from"]
TWILIO_VERIFIED_NUMBER = os.environ["twilio_to"]

my_email = os.environ["smtp_email"]
password = os.environ["smtp_password"]


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# --- This method is used to send SMS using Twilio API --- #

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )

        print(message.sid)

# --- This method is used to send emails using SMTP --- #

    def send_emails(self, emails, message, google_link):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            for email in emails:
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=email,
                    msg=f"Subject:New low price flight!\n\n{message}\n\n{google_link}".encode('utf-8')
                )