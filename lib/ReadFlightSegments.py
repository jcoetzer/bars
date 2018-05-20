# @file ReadFlightSegments.py

import os
import sys
import psycopg2
import time
from datetime import datetime, timedelta, date
from FlightData import FlightData
from BarsLog import printlog, get_verbose
from ReadDateTime import ReadDate


def ReadSegmentStatus(conn, flight_number, flight_date):

    print "Segment status for flight %s board date %s [segment_status]" \
        % (flight_number, flight_date.strftime("%Y-%m-%d"))
    RcSql = \
        "SELECT city_pair_no,selling_cls_code,status_type,segm_status_code,leg_status_code,processing_flg" \
        " FROM segment_status" \
        " WHERE flight_number='%s'" \
        " AND flight_date='%s'" \
        % (flight_number, flight_date.strftime("%m/%d/%Y"))
    printlog(RcSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    for row in cur:
        print "\tcity pair %3d class %s status type %s status code %s processed %s" \
            % (row['city_pair_no'], row['selling_cls_code'], row['status_type'], row['segm_status_code'], row['processing_flg'])


def ReadFlightPax(conn, aFlightNumber, aFlightDate):
    """Read bookings and passengers for flight."""
    print("Passengers for flight %s date %s" % (aFlightNumber, aFlightDate))
    fpSql = """
        SELECT it.book_no, bo.origin_address, it.depr_airport, it.arrv_airport, it.departure_time, it.arrival_time, pa.passenger_name,
        it.selling_cls_code, it.request_nos, pa.request_nos, pa.passenger_no, pa.pass_code, pa.passenger_no, bo.no_of_seats, group_name
        FROM  flight_segm_date as fsd
        inner join itenary as it on it.flight_number = fsd.flight_number AND it.flight_date = fsd.board_date AND it.depr_airport = fsd.depr_airport AND it.arrv_airport = fsd.arrv_airport
        inner join book as bo on bo.book_no = it.book_no inner join passenger as pa on pa.book_no = it.book_no
        inner join action_codes as ac on substr(it.reserve_status,1,2) = ac.action_code AND ac.pnl_adl_flag = 'Y'
        where fsd.flight_number= '%s' AND fsd.board_date = '%s'
        and it.itenary_type <> 'I' AND pa.passenger_no > 0 AND pa.pass_code <> 'INF' AND it.itenary_stat_flag <> 'X' AND
        bo.booking_status <> 'X' ORDER BY it.book_no, pa.passenger_name""" \
        % (aFlightNumber, aFlightDate.strftime('%Y-%m-%d'))
    printlog(2, fpSql)
    cur = conn.cursor()
    cur.execute(fpSql)
    for row in cur:
        print("\t%d\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s" %
              (row[0], row[1], row[2],
               row[3], row[4], row[5],
               row[6], row[7], row[11]))
    cur.close()
