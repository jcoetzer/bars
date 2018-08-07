# @file ReadFlightSegments.py

import os
import sys
import logging
import psycopg2
from psycopg2 import extras
import time
from datetime import datetime, timedelta, date
, get_verbose
from ReadDateTime import ReadDate

logger = logging.getLogger("web2py.app.bars")


def ReadSegmentStatus(conn, flight_number, flight_date):

    print("Segment status for flight %s board date %s [segment_status]"
          % (flight_number, flight_date.strftime("%Y-%m-%d")))
    RcSql = \
        "SELECT city_pair,selling_class,status_type,segm_status_code,leg_status_code,processing_flag" \
        " FROM segment_status" \
        " WHERE flight_number='%s'" \
        " AND flight_date='%s'" \
        % (flight_number, flight_date.strftime("%Y-%m-%d"))
    logger.debug(RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    for row in cur:
        print("\tcity pair %3d class %s status type %s status code %s processed %s" \
            % (row['city_pair'], row['selling_class'], row['status_type'], row['segm_status_code'], row['processing_flag']))


def ReadFlightPax(conn, aFlightNumber, aFlightDate):
    """Read bookings and passengers for flight."""
    print("Passengers for flight %s date %s" % (aFlightNumber, aFlightDate))
    fpSql = """
        SELECT it.book_no, bo.origin_address, it.departure_airport, it.arrival_airport, it.departure_time, it.arrival_time, pa.pax_name,
        it.selling_class, it.request_nos, pa.request_nos, pa.passenger_no, pa.pax_code, pa.passenger_no, bo.no_of_seats, group_name
        FROM  flight_segment_dates as fsd
        inner join itineraries as it on it.flight_number = fsd.flight_number AND it.flight_date = fsd.board_date AND it.departure_airport = fsd.departure_airport AND it.arrival_airport = fsd.arrival_airport
        inner join bookings as bo on bo.book_no = it.book_no
        inner join passengers as pa on pa.book_no = it.book_no
        inner join action_codes as ac on substr(it.reserve_status,1,2) = ac.action_code AND ac.pnl_adl_flag = 'Y'
        where fsd.flight_number= '%s' AND fsd.board_date = '%s'
        and it.itinerary_type <> 'I' AND pa.passenger_no > 0 AND pa.pax_code <> 'INF' AND it.status_flag <> 'X' AND
        bo.status_flag <> 'X' ORDER BY it.book_no, pa.pax_name""" \
        % (aFlightNumber, aFlightDate.strftime('%Y-%m-%d'))
    logger.debug(fpSql)
    cur = conn.cursor()
    cur.execute(fpSql)
    for row in cur:
        print("\t%d\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s" %
              (row[0], row[1], row[2],
               row[3], row[4], row[5],
               row[6], row[7], row[11]))
    cur.close()
