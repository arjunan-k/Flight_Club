import requests
import os

SHEETY_PRICES_ENDPOINT = os.environ["spe"]
sheety_header = {
    "Authorization": f'Bearer {os.environ["sh"]}'
}
SHEETY_USER_ENDPOINT = os.environ["sue"]
user_header = {
  "Authorization": f'Bearer {os.environ["sh"]}'
}


class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.user_data = {}

# --- To get the data from Google sheets using SHEETY API --- #

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=sheety_header)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

# --- To update the Google sheets using PUT IN SHEETY API --- #

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=sheety_header
            )
            print(response.text)

# --- To get the customer/user emails from Google sheets using SHEETY API --- #

    def get_customer_emails(self):
        response = requests.get(url=SHEETY_USER_ENDPOINT, headers=user_header)
        data = response.json()
        self.user_data = data["users"]
        return self.user_data