# @file ReadSchedPeriod.py

import os
import sys
import psycopg2
from psycopg2 import extras
import time
from datetime import datetime, timedelta, date
from BarsLog import blogger, get_verbose
from ReadDateTime import ReadTime
from Flight.FlightData import FlightPeriod


def ReadFlightPeriods(conn, flightNumber, dt1, dt2):

    blogger.info("Flight periods from %s to %s (flight %s)"
        % (dt1.strftime("%Y-%m-%d"), dt2.strftime("%Y-%m-%d"), str(flightNumber or 'all')), 1)
    fperds = []
    startDate = dt1.strftime("%Y-%m-%d")
    endDate = dt2.strftime("%Y-%m-%d")
    SpSql = \
        "SELECT flight_number,start_date,end_date,frequency_code,schedule_period_no" \
        " FROM flight_periods" \
        " WHERE start_date<='%s'" \
        " AND end_date>='%s'" \
        " AND flgt_sched_status='A'" \
            % (startDate, endDate)
    if flightNumber is not None:
        SpSql += \
            " AND flight_number LIKE '%s'" % flightNumber
    blogger.debug(SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur3 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)
    for row in cur:
        fn = row['flight_number']
        spn = int(row['schedule_period_no'])
        SpSql2 = \
            "SELECT DISTINCT fps.aircraft_code aircraft, fsd.departure_airport departure_city, fsd.arrival_airport arrival_airport," \
            " departure_time, arrival_time" \
            " FROM flight_perd_segm fps, flight_segment_dates fsd" \
            " WHERE fps.flight_number = '%s' AND fps.schedule_period_no = %d" \
            " AND fps.flight_number = fsd.flight_number" \
            " AND fps.schedule_period_no = fsd.schedule_period_no" \
                % ( fn, spn )
        blogger.debug(SpSql2)
        cur2.execute(SpSql2)
        for row2 in cur2:
            SpSql3 = \
                "SELECT DISTINCT dup_flight_number FROM flight_shared_leg WHERE flight_number = '%s' AND schedule_period_no = %d" \
                    % ( fn, spn )
            blogger.debug(SpSql3)
            cur3.execute(SpSql3)
            codeshares = []
            for row3 in cur3:
                codeshare = row3['dup_flight_number']
                codeshares.append(codeshare)
            fp = FlightPeriod(fn, row['start_date'], row['end_date'], row['frequency_code'], spn,
                              row2['departure_city'], int(row2['departure_time']),
                              row2['arrival_airport'], int(row2['arrival_time']),
                              row2['aircraft'], codeshares)
            fperds.append(fp)

    return fperds


def ReadFlightPeriodsLatest(conn, flightNumber, dt1, dt2):

    blogger.info("Flight periods (flight %s)" \
        % (str(flightNumber or 'all')), 1)
    fperds = []
    SpSql = \
        "SELECT flight_number,max(end_date) med" \
        " FROM flight_periods" \
        " WHERE flgt_sched_status='A'"
    if flightNumber is not None:
        SpSql += \
            " AND flight_number LIKE '%s'" \
                % (flightNumber)
    if dt1 is not None:
        SpSql += \
            " AND end_date >= '%s'" \
                % ( dt1.strftime("%Y-%m-%d") )
    if dt2 is not None:
        SpSql += \
            " AND end_date <= '%s'" \
                % ( dt2.strftime("%Y-%m-%d") )
    SpSql += \
        " GROUP BY flight_number"
    blogger.debug(SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur3 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)
    for row in cur:
        fn = row['flight_number']
        end_date = row['med']
        SpSql1 = \
            "SELECT start_date,end_date,frequency_code,schedule_period_no" \
            " FROM flight_periods" \
            " WHERE flight_number='%s'" \
            " AND flgt_sched_status='A'" \
            " AND end_date='%s'" \
                % ( fn, end_date.strftime("%Y-%m-%d") )
        blogger.debug(SpSql1)
        cur1.execute(SpSql1)
        for row1 in cur1:
            spn = int(row1['schedule_period_no'])
            blogger.info("Flight %s start %s end %s frequency %s (schedule period %d)" % ( fn, row1['start_date'], end_date, row1['frequency_code'], spn), 1)
            SpSql2 = \
                "SELECT DISTINCT fps.aircraft_code aircraft, fsd.departure_airport departure_city, fsd.arrival_airport arrival_airport," \
                " departure_time, arrival_time" \
                " FROM flight_perd_segm fps, flight_segment_dates fsd" \
                " WHERE fps.flight_number = '%s' AND fps.schedule_period_no = %d" \
                " AND fps.flight_number = fsd.flight_number" \
                " AND fps.schedule_period_no = fsd.schedule_period_no" \
                    % ( fn, spn )
            blogger.debug(SpSql2)
            cur2.execute(SpSql2)
            for row2 in cur2:
                SpSql3 = \
                    "SELECT DISTINCT dup_flight_number FROM flight_shared_leg WHERE flight_number = '%s' AND schedule_period_no = %d" \
                        % ( fn, spn )
                blogger.debug(SpSql3)
                cur3.execute(SpSql3)
                codeshares = []
                for row3 in cur3:
                    codeshare = row3['dup_flight_number']
                    codeshares.append(codeshare)
                fp = FlightPeriod(fn, row1['start_date'], row1['end_date'], row1['frequency_code'], spn,
                                row2['departure_city'], int(row2['departure_time']),
                                row2['arrival_airport'], int(row2['arrival_time']),
                                row2['aircraft'], codeshares)
                fperds.append(fp)

    return fperds


def isMarketingOrOperational(conn, flightNumber, dt1, dt2, frequency=None):

    startDate = dt1.strftime("%Y-%m-%d")
    endDate = dt2.strftime("%Y-%m-%d")
    SpSql = \
        "SELECT COUNT(*) mif" \
        " FROM flight_shared_leg fsl, city_pair cp, flight_segment_dates fsd" \
        " WHERE fsl.dup_flight_number = '%s'" \
        "  AND fsl.flight_date BETWEEN '%s' AND '%s'" \
        "  AND fsl.departure_airport = cp.departure_city" \
        "  AND fsl.arrival_airport = cp.arrival_airport" \
        "  AND fsd.flight_number = fsl.dup_flight_number" \
        "  AND fsd.city_pair = cp.city_pair" \
        "  AND fsl.flight_date = fsd.flight_date" \
            % ( flightNumber, startDate, endDate)
    if frequency is not None:
        SpSql += \
            "  AND WEEKDAY(fsd.flight_date)::CHAR IN ('%s','%s','%s','%s','%s','%s','%s')" \
                % (frequency[0], frequency[1], frequency[2], frequency[3],
                   frequency[4], frequency[5], frequency[6] )
    blogger.debug(SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)

    marketingInFlightSharedLeg =  None
    for row in cur:
        marketingInFlightSharedLeg = int(row['mif'])

    blogger.info("Found %d marketing flights for flight %s from %s to %s" \
             % (marketingInFlightSharedLeg, flightNumber, startDate, endDate))


def ReadConfigNumberOfSeats(conn, AircraftCode, haveClassCode=1,
                            yClassCode='C', ClassCode='Y'):

    blogger.info("Read configuration for aircraft code %s [aircraft_config]"
             % AircraftCode)
    #SpSql = \
        #"SELECT first 1 config_table, seat_capacity"
        #"  FROM aircraft_config"
        #"  WHERE aircraft_code = '%s'"
        #"  AND seat_capacity ="
        #"   ( SELECT MAX ( seat_capacity )"
        #"            FROM aircraft_config"
        #"           WHERE aircraft_code = '%s'"
        #"             AND selling_class = DECODE ( '%s', 0, '%s', '%s' ))"
    SpSql = \
        "SELECT config_table, seat_capacity" \
        "  FROM aircraft_config" \
        "  WHERE aircraft_code = '%s'" \
        "  AND seat_capacity =" \
        "   ( SELECT MAX ( seat_capacity )" \
        "            FROM aircraft_config" \
        "           WHERE aircraft_code = '%s')"  \
            % (AircraftCode, AircraftCode)

    blogger.debug(SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)
    ConfigTableNo = 0
    NoOfSeats = 0
    n = 0
    for row in cur:
        ConfigTableNo = str(row['config_table'])
        NoOfSeats =  int(row['seat_capacity'] or 0)
        blogger.info("\t config table number %s seats %d"
                 % (ConfigTableNo, NoOfSeats))
        n += 1

    if n == 0:
        blogger.info("\t not found")

    return ConfigTableNo, NoOfSeats


def CheckSchedPeriod(conn, dt1, dt2, alteredFrequency,
                    flightNumber, freqCode, newViacities, aircraftConfig):

    startDate = dt1.strftime("%Y-%m-%d")
    endDate = dt2.strftime("%Y-%m-%d")
    blogger.info("Check schedule period from %s to %s freq %s (%s) flight %s via %s aircraft %s [flight_periods]"
        % (startDate, endDate, alteredFrequency, freqCode, flightNumber,
           newViacities, aircraftConfig))

    SpSql = \
        "SELECT fp.frequency_code fc, fp.schedule_period_no spn," \
         "   fp.flgt_sched_status fss, fp.start_date fps,fp.end_date fpe" \
         " FROM flight_periods fp" \
         " WHERE " \
         "   end_date<=('%s')::DATE-1 UNITS DAY" \
         "   AND '%s' NOT BETWEEN fp.start_date AND fp.end_date" \
         "   AND '%s' NOT BETWEEN fp.start_date AND fp.end_date" \
         "   AND fp.flight_number='%s'" \
             % (startDate, startDate, endDate, flightNumber)
    blogger.debug(SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)
    for row in cur:
        blogger.info("Freq %s period %3s status %s start %s end %s"
            % (row['fc'], row['spn'], row['fss'], row['fps'], row['fpe']))


def ReadSchedPeriod(conn, dt1, dt2, alteredFrequency,
                    flightNumber, freqCode, newViacities, aircraftConfig):

    startDate = dt1.strftime("%Y-%m-%d")
    endDate = dt2.strftime("%Y-%m-%d")
    blogger.info("Read schedule period from %s to %s freq %s (alter %s) flight %s via %s aircraft %s [flight_periods, flight_segment_dates, flight_perd_legs]" \
        % (startDate, endDate, freqCode, alteredFrequency, flightNumber,
           newViacities, aircraftConfig))
    SpSql = \
         "SELECT FIRST 1 fsd.schedule_period_no spn" \
         " FROM flight_periods fp, flight_segment_dates fsd, flight_perd_legs fpl" \
         "  GROUP BY fp.flight_number, fp.start_date,fp.end_date," \
         "   fp.frequency_code, fp.schedule_period_no," \
         "   fp.flgt_sched_status, fsd.flight_number," \
         "   fsd.flight_date, fsd.flgt_sched_status," \
         "   fsd.schedule_period_no, fp.via_cities," \
         "   fpl.flight_number , fpl.schedule_period_no," \
         "   fpl.config_table" \
         "  HAVING fp.end_date=MAX(fp.end_date)" \
         "   AND end_date<=('%s')::DATE-1 UNITS DAY" \
         "   AND '%s' NOT BETWEEN fp.start_date AND fp.end_date" \
         "   AND '%s' NOT BETWEEN fp.start_date AND fp.end_date" \
         "   AND fp.flight_number=fsd.flight_number" \
         "   AND fpl.flight_number=fsd.flight_number" \
         "   AND fp.schedule_period_no=fsd.schedule_period_no" \
         "   AND fpl.schedule_period_no=fsd.schedule_period_no" \
         "   AND fp.flgt_sched_status=fsd.flgt_sched_status" \
         "   AND fsd.flight_date NOT BETWEEN '%s' AND '%s'" \
         "   AND (SELECT COUNT(flight_date) FROM flight_segment_dates WHERE flight_date BETWEEN '%s' AND '%s' AND flight_number = fp.flight_number ) = 0" \
         "   AND fp.end_date + 7 > '%s'" \
         "   AND (WEEKDAY('%s'))::CHAR IN('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
         "   AND fp.flgt_sched_status IN('A','S')" \
         "   AND fp.flight_number='%s'" \
         "   AND fp.frequency_code='%s'" \
         "   AND fp.via_cities='%s'" \
         "   AND fpl.config_table='%s'" \
        % (startDate, startDate, endDate,
           startDate, endDate,
           startDate, endDate,
           startDate, startDate,
           alteredFrequency[0],
           alteredFrequency[1],
           alteredFrequency[2],
           alteredFrequency[3],
           alteredFrequency[4],
           alteredFrequency[5],
           alteredFrequency[6],
           flightNumber, freqCode, newViacities, aircraftConfig)
    blogger.debug(SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)
    n = 0
    for row in cur:
        blogger.info("\t schedule period %s" % row['spn'])
        n += 1

    if n == 0:
        blogger.info("\t not found")

    return n


def DatesConsecutiveByFrequency(conn, flight_number, dt1, schedule_period_no):

    blogger.info("Dates for flight %s date %s period %s [flight_periods]"
        % (flight_number, dt1, str(schedule_period_no)))
    startDate = dt1.strftime("%Y-%m-%d")
    SpSql = \
        "SELECT WEEKDAY(end_date) ed, WEEKDAY('%s') sd" \
         " FROM flight_periods" \
         " WHERE flight_number='%s'" \
         " AND schedule_period_no=%d" \
         " AND flgt_sched_status IN ( 'A', 'S' )" \
             % (startDate, flight_number, schedule_period_no)
    blogger.debug(SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)
    for row in cur:
        blogger.info("\tStart %s end %s" % (row['sd'], row['ed']))
