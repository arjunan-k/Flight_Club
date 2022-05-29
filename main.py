from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "LON"

# --- Adding the IataCode in the missing rows by calling Tequila fligh search API --- #

for item in sheet_data:
    if item['iataCode'] == "":
        for row in sheet_data:
            row["iataCode"] = flight_search.get_destination_code(row["city"])
        data_manager.destination_data = sheet_data
        data_manager.update_destination_codes()

    tomorrow = datetime.now() + timedelta(days=1)
    six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# --- Calling flight search API, to find flights and sending the details in SMS and Email by including links --- #

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight is None:
        continue
    if flight.price < destination["lowestPrice"]:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]
        text = f"Low price alert! £{flight.price} to fly from {flight.origin_city}-" \
               f"{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from " \
               f"{flight.out_date} to {flight.return_date}."
        notification_manager.send_sms(
            message=text
        )
        if flight.stop_overs > 0:
            text += f"\n\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}." \
                   f"{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}\n\n" \
                   f"{flight.link}"
            notification_manager.send_emails(emails, text, link)