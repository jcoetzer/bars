

class AircraftData(object):
    """Aircraft configuration."""
    company_code = ''
    aircraft_code = ''
    config_table = ''
    tail_number = ''
    cabin_codes = []
    seat_capacities = []

    def __init__(self,
                 company_code,
                 aircraft_code,
                 config_table,
                 tail_number,
                 cabin_codes,
                 seat_capacities):
        self.company_code = company_code
        self.aircraft_code = aircraft_code
        self.config_table = config_table
        self.tail_number = tail_number
        self.cabin_codes = cabin_codes
        self.seat_capacities = seat_capacities

    def display(self):
        print("Aircraft %s config %s tail %s cabin %s seats %s"
              % (self.aircraft_code,
                 self.config_table,
                 self.tail_number,
                 self.cabin_codes,
                 self.seat_capacities))
