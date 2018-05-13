# @file FlightData.py


import os
import sys
import psycopg2
import time
from datetime import datetime, timedelta, date
from BarsLog import printlog, get_verbose
from ReadDateTime import ReadTime


class FlightData(object):

    board_dts      = None
    board_dow      = ''
    board_date_mdy = ''
    board_date_iso = ''
    departure_airport = ''
    departure_time = None
    departure_terminal = 'X'
    arrival_airport = ''
    arrival_time = None
    arrival_terminal = 'X'
    reserve_status = ''
    board_date_iata = ''
    board_weekday = 0
    aircraft_code = ''
    seat_capacity = 0
    journey_time  = 0
    departure_ts = ''
    arrival_ts = ''
    codeshare = None
    schd_perd_no = 0

    def __init__(self, 
                 class_code, 
                 flight_number, 
                 departure_date,
                 departure_time, 
                 arrival_time, 
                 departure_airport, 
                 arrival_airport, 
                 city_pair_no,
                 company_code='JE',
                 aircraft_code='', 
                 schd_perd_no=0,
                 codeshare=None):
        printlog(2, "New flight %s board %s class %s depart %s arrive %s" \
                 " from %s to %s (pair %s) aircraft %s" \
            % ( flight_number, departure_date.strftime("%Y-%m-%d"), class_code,
                departure_time, arrival_time, \
                departure_airport, arrival_airport, city_pair_no,
                aircraft_code))
        self.class_code         = class_code
        #self.company_code       = company_code
        self.flight_number      = flight_number
        if flight_number is None:
            self.company_code   = ''
            self.flight_integer = 0
        else:
            self.company_code   = flight_number[0:2]
            self.flight_integer = int(flight_number[2:])
        if departure_date is not None:
            self.board_dts = departure_date
            self.board_dow = self.board_dts.strftime("%a")
            self.board_date_mdy = self.board_dts.strftime("%m/%d/%Y")
            self.board_date_iso = self.board_dts.strftime("%Y-%m-%d")
            self.board_date_iata = self.board_dts.strftime("%d%b%y").upper()
            # Weekday as a decimal number 0(Sunday), 1(Monday) to 6(Saturday)
            self.board_weekday = int(self.board_dts.strftime("%w"))
            # Convert to 1(Monday) to 7(Sunday)
            if self.board_weekday == 0:
                self.board_weekday = 7
        # Times are in minutes since midnight
        if departure_time is not None:
            self.departure_time = ReadTime(departure_time) #, self.board_date_iso)
            self.departure_ts = str("%02d:%02d" \
                % (self.departure_time.tm_hour, self.departure_time.tm_min))
        if arrival_time is not None:
            self.arrival_time = ReadTime(arrival_time) # , self.board_date_iso)
            self.arrival_ts = str("%02s:%02d" \
                % (self.arrival_time.tm_hour, self.arrival_time.tm_min))
        self.departure_airport  = str(departure_airport or '').strip()
        self.arrival_airport    = str(arrival_airport or '').strip()
        self.city_pair_no       = city_pair_no
        if aircraft_code is not None:
            self.aircraft_code      = str(aircraft_code)
        if schd_perd_no is not None:
            self.schd_perd_no = int(schd_perd_no)

    def update_times(self, departure_time, arrival_time, journey_time=0):
        printlog(2, "Update flight depart %s arrive %s" \
            % (departure_time, arrival_time))
        self.departure_time = ReadTime(departure_time, self.board_date_iso)
        self.departure_ts = str("%02d:%02d" \
            % (self.departure_time.tm_hour, self.departure_time.tm_min))
        self.arrival_time = ReadTime(arrival_time, self.board_date_iso)
        self.arrival_ts = str("%02s:%02d" \
            % (self.arrival_time.tm_hour, self.arrival_time.tm_min))
        self.journey_time = journey_time

    def update_aircraft(self, aircraft_code, seat_capacity):
        self.aircraft_code      = str(aircraft_code)
        self.seat_capacity      = seat_capacity

    def update_reserve_status(self, reserve_status):
        self.reserve_status = reserve_status

    def update_codeshare(self, codeshare):
        self.codeshare = codeshare
        printlog(2, "Codeshare set to %s" % self.codeshare)

    def display(self, eol=True, prefix=''):
        print "%sFlight %6s board %s %s from %s to %s" % \
            (prefix, self.flight_number, self.board_dow, self.board_date_iso,
             self.departure_airport, self.arrival_airport),
        if self.city_pair_no != 0:
            print " (city pair %4d)" % self.city_pair_no,
        if self.departure_time is not None and self.arrival_time is not None:
            print "departs %02d:%02d arrives %02d:%02d" \
                % (self.departure_time.tm_hour, self.departure_time.tm_min,
                   self.arrival_time.tm_hour, self.arrival_time.tm_min),
        elif self.departure_time is not None:
            print "departs %02d:%02d" \
                % (self.departure_time.tm_hour, self.departure_time.tm_min),
        if self.journey_time is not None and self.journey_time > 0:
            print "(%-3d minutes)" % self.journey_time,
        if len(self.aircraft_code) > 0:
            print "aircraft code %4s" % self.aircraft_code,
        if self.seat_capacity > 0:
            print "(%-3d seats)" % self.seat_capacity,
        print "%s" % self.reserve_status,
        if len(self.reserve_status):
            if 'X' in self.reserve_status:
                print "(inactive)",
        if self.codeshare is not None:
            print "codeshare %6s" % self.codeshare,
        if self.schd_perd_no != 0:
            print "schedule period %6d" % self.schd_perd_no,
        if eol : print


def FindFlight(flights, flight_number):
    n = 0
    for flight in flights:
        if flight.flight_number == flight_number:
            return n
        n += 1
    return -1


class FlightPeriod(object):

    flight_number = None
    start_date = None
    end_date = None
    frequency_code = None
    schd_perd_no = 0
    aircraft_code = None
    departure_time = None
    arrival_time = None
    codeshares = []

    def __init__(self, flight_number, start_date, end_date, frequency_code, schd_perd_no,
                 departure_airport, departure_time, arrival_airport, arrival_time,
                 aircraft_code, codeshares):
        self.flight_number = flight_number
        self.start_date = start_date
        self.end_date = end_date
        self.frequency_code = frequency_code
        self.schd_perd_no = int(schd_perd_no)
        self.departure_airport = departure_airport
        self.departure_time = int(departure_time)
        self.arrival_airport = arrival_airport
        self.departure_time = int(departure_time)
        self.arrival_time = int(arrival_time)
        self.aircraft_code = aircraft_code
        self.codeshares = codeshares

    def display(self):
        print "Flight %6s start %s end %s frequency %s depart %s %02d:%02d arrive %s %02d:%02d aircraft %s (schedule period %4d)" \
            % ( self.flight_number, self.start_date, self.end_date, self.frequency_code,
                self.departure_airport, self.departure_time/60, self.departure_time%60,
                self.arrival_airport, self.arrival_time/60, self.arrival_time%60,
                self.aircraft_code,
                self.schd_perd_no ),
        for codeshare in self.codeshares:
            print "%s" % codeshare,
        print

    def displaycsv(self):
        sys.stdout.write("%s,%s,%s,%s,%s,%02d%02d,%s,%02d%02d,%s,%d" \
            % ( self.flight_number, self.start_date.strftime("%d%b%Y").upper(), self.end_date.strftime("%d%b%Y").upper(),
                self.frequency_code.replace('-', ''),
                self.departure_airport, self.departure_time/60, self.departure_time%60,
                self.arrival_airport, self.arrival_time/60, self.arrival_time%60,
                self.aircraft_code,
                self.schd_perd_no ))
        for codeshare in self.codeshares:
            sys.stdout.write(",%s" % codeshare)
        sys.stdout.write("\n")

