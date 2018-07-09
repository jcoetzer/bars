# @file ReadFlightTimes.py

import sys
import psycopg2
from psycopg2 import extras
from BarsLog import set_verbose, get_verbose, printlog
from ReadDateTime import ReadDate


def ReadFlightTimes(conn, flight):

    print("Flight periods for flight %s date %s" %
        ( flight.flight_number, flight.board_date_iso ))
    FtSql = \
        "SELECT schedule_period_no, start_date, end_date" \
        " FROM flight_periods" \
        " WHERE flight_number = '%s'" \
            % ( flight.flight_number )
        #" AND start_date = '%s'" \
        #" AND end_date = '%s'" \
        #" AND frequency_code = '%s'" \
    printlog(FtSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FtSql)
    schedule_period_no = 0
    start_date = None
    end_date = None
    for row in cur:
        start_date = row['start_date']
        end_date = row['end_date']
        printlog("Start %s end %s schedule period %d"
            % ( start_date, end_date, row['schedule_period_no'] ), 2)
        if flight.board_dts.date() >= start_date and flight.board_dts.date() <= end_date:
            schedule_period_no = row['schedule_period_no']
            print("Schedule period %d start %s end %s" \
                % ( schedule_period_no, start_date, end_date ))

    return schedule_period_no, start_date, end_date


def ReadFlightPerdLegsTimes(conn, flight, SchdPerdNo):

    print("Flight period legs for flight %s date %s (schedule period %d)" %
        ( flight.flight_number, flight.board_date_iso, SchdPerdNo ))
    FtSql = \
        "SELECT departure_time, arrival_time" \
        " FROM flight_perd_legs" \
        " WHERE flight_number = '%s'" \
        " AND schedule_period_no = %d" \
            % ( flight.flight_number, SchdPerdNo )
    printlog(FtSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FtSql)
    for row in cur:
        departure_time = "%02d:%02d" \
            % ( int(row['departure_time']/60), int(row['departure_time']%60) )
        arrival_time = "%02d:%02d" \
            % ( int(row['arrival_time']/60), int(row['arrival_time']%60) )
        print("\tDepart %s arrive %s" \
            % ( departure_time, arrival_time ))

def ReadFlightSegmDateTimes(conn, flight, SchdPerdNo):

    print("Flight segment date times for flight %s date %s (schedule period %d)" %
        ( flight.flight_number, flight.board_date_iso, SchdPerdNo ))
    FtSql = \
        "SELECT DISTINCT departure_time, arrival_time" \
        " FROM flight_segment_dates" \
        " WHERE flight_number = '%s'" \
        " AND schedule_period_no = %d" \
            % ( flight.flight_number, SchdPerdNo )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FtSql)
    for row in cur:
        departure_time = "%02d:%02d" \
            % ( int(row['departure_time']/60), int(row['departure_time']%60) )
        arrival_time = "%02d:%02d" \
            % ( int(row['arrival_time']/60), int(row['arrival_time']%60) )
        print("\tDepart %s arrive %s" \
            % ( departure_time, arrival_time ))


def ReadFlightSegmDates(conn, flight, SchdPerdNo):

    print("Flight segment dates for flight %s date %s (schedule period %d)" %
        ( flight.flight_number, flight.board_date_iso, SchdPerdNo ))
    FtSql = \
        "SELECT DISTINCT flight_date" \
        " FROM flight_segment_dates" \
        " WHERE flight_number = '%s'" \
        " AND schedule_period_no = %d" \
            % ( flight.flight_number, SchdPerdNo )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FtSql)
    flight_segment_datess = []
    for row in cur:
        flight_segment_datess.append(row['flight_date'])

    return flight_segment_datess


def ReadFlightDateLegTimes(conn, flight, flight_dates):

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for flight_date in flight_dates:
        print("Flight date legs for flight %s date %s"
            % ( flight.flight_number, flight_date.strftime("%Y-%m-%d") ))
        FtSql = \
            "SELECT DISTINCT departure_time, departure_airport, arrival_airport" \
            " FROM flight_date_leg" \
            " WHERE flight_number = '%s'" \
            " AND flight_date = '%s'" \
                % ( flight.flight_number, flight_date.strftime("%Y-%m-%d") )
        cur.execute(FtSql)
        flight_segment_datess = []
        for row in cur:
            print("\tDepart %s" \
                % ( row['departure_time'].time() ))


def ReadFlightSharedLegTimes(conn, flight, flight_dates):

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for flight_date in flight_dates:
        print("Flight shared legs for flight %s date %s"
            % ( flight.flight_number, flight_date.strftime("%Y-%m-%d") ))
        FtSql = \
            "SELECT departure_time, arrival_time, schedule_period_no" \
            " FROM flight_shared_leg" \
            " WHERE ( flight_number = '%s' OR dup_flight_number = '%s' )" \
            " AND flight_date = '%s'" \
                % ( flight.flight_number, flight.flight_number, flight_date.strftime("%Y-%m-%d") )
        cur.execute(FtSql)
        flight_segment_datess = []
        for row in cur:
            departure_time = "%02d:%02d" \
                % ( int(row['departure_time']/60), int(row['departure_time']%60) )
            arrival_time = "%02d:%02d" \
                % ( int(row['arrival_time']/60), int(row['arrival_time']%60) )
            print("\tDepart %s arrive %s  (schedule period %d)"
                % ( departure_time, arrival_time, row['schedule_period_no'] ))






