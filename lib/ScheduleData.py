"""Flight schedule data."""




class SsmData(object):
    """Flight schedule class."""

    departure_terminal = 'X'
    arrival_terminal = 'X'
    frequency_code = 0
    aircraft_code = '738'
    aircraft_conf = '738'
    class_codes = ['Y', 'C']
    class_seats = [186, 2]

    def __init__(self,
                 action,
                 flight_number,
                 start_date,
                 end_date,
                 frequency_code,
                 frequency_codes,
                 departure_airport,
                 departure_time,
                 arrival_airport,
                 arrival_time,
                 aircraft_code=None,
                 aircraft_conf=None,
                 aircraft_tail=None,
                 class_codes=None,
                 class_seats=None):
        """New instance."""
        self.action = action
        self.flight_number = flight_number
        self.start_date = start_date
        self.end_date = end_date
        self.frequency_code = frequency_code
        self.frequency_codes = frequency_codes
        self.departure_airport = departure_airport
        self.departure_time = departure_time
        self.arrival_airport = arrival_airport
        self.arrival_time = arrival_time
        if aircraft_code is not None:
            self.aircraft_code = aircraft_code
        if aircraft_tail is not None:
            self.aircraft_tail = aircraft_tail
        if aircraft_conf is not None:
            self.aircraft_conf = aircraft_conf
        if class_codes is not None:
            self.class_codes = class_codes
        if class_seats is not None:
            self.class_seats = class_seats

    def check(self):
        """Check data."""
        if self.action is None:
            print("action not specified")
            return False
        elif self.flight_number is None:
            print("flight_number not specified")
            return False
        elif self.start_date is None:
            print("start date not specified")
            return False
        elif self.end_date is None:
            print("end_date not specified")
            return False
        elif self.frequency_code is None and self.frequency_codes is None:
            print("frequency codes not specified")
            return False
        elif self.departure_airport is None:
            print("departure airport not specified")
            return False
        elif self.departure_time is None:
            print("departure time not specified")
            return False
        elif self.arrival_airport is None:
            print("arrival airport not specified")
            return False
        elif self.arrival_time is None:
            print("arrival airport not specified")
            return False
        elif self.aircraft_code is None:
            print("aircraft code not specified")
            return False
        elif self.aircraft_conf is None:
            print("aircraft conf not specified")
            # return False
        elif self.aircraft_tail is None:
            print("aircraft tail number not specified")
            return False
        elif self.class_codes is None:
            print("class codes not specified")
            return False
        elif self.class_seats is None:
            print("class seats not specified")
            return False
        else:
            logger.info("Flight data is OK")

        logger.info("Flight %s start %s end %s"
                 % (self.flight_number,
                    self.start_date.strftime("%Y-%m-%d"),
                    self.end_date.strftime("%Y-%m-%d")))
        return True

    def display(self):
        """Display data."""
        print("Flight %s start %s end %s frequency %d"
              " depart %s %s arrive %s %s"
              " aircraft %s cabin %s classes %s action %s"
              % (self.flight_number, self.start_date, self.end_date,
                 self.frequency_code,
                 self.departure_airport, self.departure_time,
                 self.arrival_airport, self.arrival_time,
                 self.aircraft_code, self.aircraft_conf,
                 self.class_codes, self.action))
