from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight

data_manager = DataManager()
flight_search = FlightSearch()

sheet_data = data_manager.get_sheet_data()

# Adding IATA codes to each city in Google Sheet
for row in sheet_data:
    if row['iataCode'] == '':
        iata_code = flight_search.get_iata_code(row['city'])
        row['iataCode'] = iata_code

data_manager.sheet_data = sheet_data
data_manager.update_sheet()

# Searching for Flights
for city in sheet_data:
    print(f"Looking for flights to {city['city']}")
    flights = flight_search.get_flight_offers(
        city['iataCode']
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{city['city']}: ${cheapest_flight.price}")
