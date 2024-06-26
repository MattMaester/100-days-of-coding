from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_sheet_data()

# Adding IATA codes to each city in Google Sheet
for row in sheet_data:
    if row['iataCode'] == '':
        iata_code = flight_search.get_iata_code(row['city'])
        row['iataCode'] = iata_code

data_manager.sheet_data = sheet_data
data_manager.update_sheet()
all_users = data_manager.get_customer_emails()
emails_list = [user["what'sYourEmail?"] for user in all_users]

# Searching for Flights
for city in sheet_data:
    print(f"Looking for flights to {city['city']}")
    flights = flight_search.get_flight_offers(city['iataCode'])
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{city['city']}: ${cheapest_flight.price}")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < city['lowestPrice']:
        if cheapest_flight == 0:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"with {cheapest_flight.stops} stop(s) " \
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        print(f"Check your email. Lower price flight found to {city['city']}!")

        notification_manager.send_whatsapp(message)
        notification_manager.send_emails(email_list=emails_list, message=message)


