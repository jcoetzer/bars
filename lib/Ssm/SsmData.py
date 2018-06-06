# @file SsmData.py

import re
from BarsLog import printlog
from ReadDateTime import ReadDate, ReadTime

action = None
time_zone = None
flight_number = None
leg_depart = None
leg_arrive = None
start_date = None
end_date = None
frequency_code = None
frequency_codes = []
segments = {}
aircraft_code = None
aircraft_conf = []
aircraft_tail = None
departure_airport = None
arrival_airport = None
departure_time = None
arrival_time = None
class_codes = []
class_seats = []


# Set action
def set_action(atype):
    global action
    action = atype
    printlog(2, "Action %s" % (action))


# Set time zone
def set_time_zone(atz):
    global time_zone
    time_zone = atz
    printlog(2, "Time zone %s" % (time_zone))


# Add flight number
def add_flight_number(afnum, airline, fd1=None, fd2=None, fd3=None):
    global flight_number
    flight_number = afnum
    printlog(2, "Flight %s" % (flight_number))


def add_leg(depart, arrive, days):
    """Add flight leg."""
    global departure_airport, departure_time, arrival_airport, arrival_time
    departure_airport = depart[0:3]
    atime = ReadTime(int(depart[3:]))
    departure_time = "%02d:%02d" % (atime.tm_hour, atime.tm_min)
    arrival_airport = arrive[0:3]
    atime = ReadTime(int(arrive[3:]))
    arrival_time = "%02d:%02d" % (atime.tm_hour, atime.tm_min)
    printlog(2, "Leg depart %s %s arrive %s %s (%s)"
             % (departure_airport, departure_time,
                arrival_airport, arrival_time, days))


def add_dates_freq(sdate, edate, freq):
    """Add dates and frequencies."""
    global start_date, end_date, frequency_code, frequency_codes
    start_date = ReadDate(sdate)
    end_date = ReadDate(edate)
    frequency_code = int(freq)
    fstr = str(freq)
    ln = len(fstr)
    n = 0
    while n < ln:
        frequency_codes.append(int(fstr[n]))
        n += 1
    printlog(2, "Start %s end %s frequency %d"
             % (sdate, edate, frequency_code))
    printlog(2, "Frequency codes %s" % frequency_codes)


# Add segment
def add_segment(deparr, adata1):
    global segments, class_codes, class_seats
    printlog(2, "Depart/arrive %s data %s" % (deparr, adata1))
    segments[deparr] = adata1
    if '/' in adata1:
        fndata = adata1.split('/')
        if fndata[0] == '106':
            cdata = fndata[1]
            class_codes = re.findall('\D+', cdata)
            printlog(2, "Class codes %s" % class_codes)
            class_seats = re.findall('\d+', cdata)
            printlog(2, "Class seats %s" % class_seats)


# Add configuration
def add_config(adata):
    printlog(2, "Configuration %s" % (adata))


# Add equipment
def add_equipment(atype, abook, atail, cdata, cdata2=None):
    global aircraft_code, aircraft_conf, aircraft_tail
    aircraft_code = atype
    aircraft_conf.append(cdata)
    if cdata2 is not None:
        aircraft_conf.append(cdata2)
    aircraft_tail = atail
    printlog(2, "Type %s book %s cabin %s tail %s"
             % (aircraft_code, abook, aircraft_conf, aircraft_tail))


def read_ssm_data():
    global action, flight_number, start_date, end_date, frequency_code, \
        frequency_codes, departure_airport, departure_time, arrival_airport, \
        arrival_time, aircraft_code, aircraft_conf, aircraft_tail, \
        class_codes, class_seats
    ssm_data = SsmData(action,
                       flight_number,
                       start_date,
                       end_date,
                       frequency_code,
                       frequency_codes,
                       departure_airport,
                       departure_time,
                       arrival_airport,
                       arrival_time,
                       aircraft_code,
                       aircraft_conf,
                       aircraft_tail,
                       class_codes,
                       class_seats)
    return ssm_data
