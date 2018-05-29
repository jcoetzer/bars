"""Itenary data."""


import os
import sys
import time
from datetime import datetime, timedelta, date
from BarsLog import printlog
from ReadDateTime import ReadDate


class ItenaryData(object):
    """Itenary data."""
    flight_number= None
    company_code = None
    flight_integer = 0
    board_dts      = None
    board_date_mdy = ''
    board_date_iso = ''
    class_code = None
    reserve_status = ''
    departure_airport = None
    arrival_airport = None
    status_flag = None
    reserve_status = None
    city_pair = None
    itenary_type = None

    def __init__(self, flight_number, departure_date, class_code,
                 departure_airport, arrival_airport,
                 status_flag, reserve_status, itenary_type=None):
        """New itenary for flight."""
        printlog("New itenary flight %s date %s class %s" \
                 " from %s to %s status %s reserve %s" \
            % ( flight_number,departure_date, class_code,
                departure_airport, arrival_airport,
                status_flag, reserve_status),2)
        self.flight_number      = str(flight_number).replace(' ', '')
        self.company_code   = flight_number[0:2]
        self.flight_integer = int(flight_number[2:])
        self.board_dts          = ReadDate(str(departure_date))
        self.board_date_mdy     = self.board_dts.strftime("%m/%d/%Y")
        self.board_date_iso     = self.board_dts.strftime("%Y-%m-%d")
        self.class_code = class_code
        self.departure_airport  = departure_airport.strip()
        self.arrival_airport    = arrival_airport.strip()
        self.status_flag       = status_flag
        self.reserve_status = reserve_status
        self.itenary_type = str(itenary_type or '?')


    def display(self):
        """Display itenary."""
        print "Itenary flight %6s date %s from %s to %s status %s reserve %s type %s" % \
            (self.flight_number, self.board_date_iso, \
             self.departure_airport, self.arrival_airport, # str(self.city_pair or ''),
             self.status_flag, self.reserve_status, self.itenary_type)





