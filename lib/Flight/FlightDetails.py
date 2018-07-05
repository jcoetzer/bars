# @file FlightDetails.py
"""
Read Flight Details.
"""

import psycopg2
from psycopg2 import extras

from BarsLog import printlog
from datetime import datetime, date

def GetFlightDetails(conn, aflight_number, aboard_date,
                     adeparture_airport, aarrival_airport):
    """Get flight details."""
    printlog(1, "Get flight %s board %s depart %s arrive %s"
             % (aflight_number, aboard_date,
                str(adeparture_airport or 'not specified'),
                str(aarrival_airport or 'not specified')))
    fdSql = \
        "SELECT fsd.flight_number, fsd.board_date, fsd.flight_date,"
        #"(fsd.board_date + interval fsd.date_change_ind days) as arrival_date," \
    fdSql += \
        """ fsd.flight_date, fsd.departure_time, fsd.arrival_time,
        cp.city_pair, cp.departure_airport, dc.city_name,
        cp.arrival_airport, ac.city_name,
        fsd.departure_airport, da.airport_name,
        fsd.arrival_airport, aa.airport_name,
        fsd.departure_terminal, dt.terminal_name,
        fsd.arrival_terminal, at.terminal_name,
        cp.distance, cp.distance_uom,
        fsd.no_of_stops,
        fsd.aircraft_code, air.description as aircraft_description, fp.start_date, fp.end_date,
        fsd.date_change_ind as date_change_indicator,
        fsd.flight_path_code
        FROM flight_segment_dates as fsd
        INNER JOIN city_pairs as cp on cp.city_pair = fsd.city_pair
        INNER JOIN flight_periods as fp on fp.flight_number = fsd.flight_number and fp.schedule_period_no = fsd.schedule_period_no
        LEFT JOIN terminal as dt on dt.airport_code = fsd.departure_airport and dt.terminal_no = fsd.departure_terminal
        LEFT JOIN terminal as at on at.airport_code = fsd.arrival_airport and at.terminal_no = fsd.arrival_terminal
        LEFT JOIN airport as da on da.airport_code = fsd.departure_airport
        LEFT JOIN airport as aa on aa.airport_code = fsd.arrival_airport
        LEFT JOIN city as dc on dc.city_code = cp.departure_airport
        LEFT JOIN city as ac on ac.city_code = cp.arrival_airport
        LEFT JOIN master_files as air on air.file_code = 'ACFT' and air.master_code = fsd.aircraft_code
        LEFT JOIN state as dps on dps.state_code = dc.state_code
        LEFT JOIN state as ars on ars.state_code = ac.state_code
        WHERE fsd.flight_number = '%s'
        AND fsd.board_date = '%s'""" \
        % (aflight_number, aboard_date )
    if adeparture_airport is not None and aarrival_airport is not None:
        fdSql += \
            """ AND fsd.departure_airport = '%s'
            AND fsd.arrival_airport = '%s'""" \
            % (adeparture_airport, aarrival_airport)
    fdSql += \
        " ORDER BY fsd.board_date, departure_time, fsd.flight_number"
    printlog(2, "%s" % fdSql)
    cur = conn.cursor()
    cur.execute(fdSql)

    printlog(2, "Selected %d row(s)" % cur.rowcount)
    for row in cur:
        flight_number = row[0]
        board_date = row[1]
        flight_date = row[2]
        arrival_date = row[3]
        departure_time = row[4]
        arrival_time = row[5]
        departure_airport = row[11]
        arrival_airport = row[13]
        distance = row[19]
        if distance is None:
            distance = 0
        no_of_stops = row[21]
        aircraft_code = row[22]
        aircraft_description = row[23]
        journey_time = datetime.combine(date.min, arrival_time) - \
            datetime.combine(date.min, departure_time)
        print("Flight %s depart %s %s %s arrive %s %s %s (%s)"
              " aircraft %s (%s) %dkm %d stops" \
              % (flight_number,
                 departure_airport, flight_date, departure_time.strftime("%H:%M"),
                 arrival_airport, arrival_date, arrival_time.strftime("%H:%M"),
                 journey_time, aircraft_description, aircraft_code, distance,
                 no_of_stops))
