"""
Itinerary data.
"""
from BarsLog import blogger

class ItineraryData(object):
    """Itinerary data."""
    flight_number = None
    company_code = None
    flight_integer = 0
    board_dts = None
    board_date_mdy = ''
    board_date_iso = ''
    class_code = None
    reserve_status = ''
    departure_airport = None
    arrival_airport = None
    status_flag = None
    reserve_status = None
    city_pair = None
    itinerary_type = None

    def __init__(self, flight_number, departure_date, class_code,
                 departure_airport, arrival_airport, city_pair,
                 status_flag, reserve_status, itinerary_type=None):
        """New itinerary for flight."""
        blogger().debug("New itinerary flight %s date %s class %s"
                      " from %s to %s status %s reserve %s"
                      % (flight_number, departure_date, class_code,
                         departure_airport, arrival_airport,
                         status_flag, reserve_status))
        self.flight_number = str(flight_number).replace(' ', '')
        self.company_code = flight_number[0:2]
        self.flight_integer = int(flight_number[2:])
        self.board_dts = departure_date
        self.board_date_mdy = self.board_dts.strftime("%m/%d/%Y")
        self.board_date_iso = self.board_dts.strftime("%Y-%m-%d")
        self.class_code = class_code
        self.departure_airport = departure_airport.strip()
        self.arrival_airport = arrival_airport.strip()
        self.city_pair = city_pair
        self.status_flag = status_flag
        self.reserve_status = reserve_status
        self.itinerary_type = str(itinerary_type or '?')

    def display(self):
        """Display itinerary."""
        print("Itinerary flight %6s date %s from %s to %s status %s"
              " reserve %s type %s"
              % (self.flight_number, self.board_date_iso,
                 self.departure_airport, self.arrival_airport,
                 self.status_flag, self.reserve_status, self.itinerary_type))

    def blog(self):
        """Log itinerary."""
        blogger().info("Itinerary flight %6s date %s from %s to %s status %s"
              " reserve %s type %s"
              % (self.flight_number, self.board_date_iso,
                 self.departure_airport, self.arrival_airport,
                 self.status_flag, self.reserve_status, self.itinerary_type))
