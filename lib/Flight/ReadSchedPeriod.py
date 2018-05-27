# @file ReadSchedPeriod.py

import os
import sys
import psycopg2
import time
from datetime import datetime, timedelta, date
from BarsLog import printlog, get_verbose
from ReadDateTime import ReadTime
from FlightData import FlightPeriod

def ReadFlightPeriods(conn, flightNumber, dt1, dt2):

    printlog(1, "Flight periods from %s to %s (flight %s)" \
        % (dt1.strftime("%Y-%m-%d"), dt2.strftime("%Y-%m-%d"), str(flightNumber or 'all')), 1)
    fperds = []
    startDate = dt1.strftime("%m/%d/%Y")
    endDate = dt2.strftime("%m/%d/%Y")
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
    printlog(2, SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur3 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)
    for row in cur:
        fn = row['flight_number']
        spn = int(row['schedule_period_no'])
        SpSql2 = \
            "SELECT DISTINCT fps.aircraft_code aircraft, fsd.departure_airport start_city, fsd.arrival_airport end_city," \
            " departure_time, arrival_time" \
            " FROM flight_perd_segm fps, flight_segm_date fsd" \
            " WHERE fps.flight_number = '%s' AND fps.schedule_period_no = %d" \
            " AND fps.flight_number = fsd.flight_number" \
            " AND fps.schedule_period_no = fsd.schedule_period_no" \
                % ( fn, spn )
        printlog(2, SpSql2)
        cur2.execute(SpSql2)
        for row2 in cur2:
            SpSql3 = \
                "SELECT DISTINCT dup_flight_number FROM flight_shared_leg WHERE flight_number = '%s' AND schedule_period_no = %d" \
                    % ( fn, spn )
            printlog(2, SpSql3)
            cur3.execute(SpSql3)
            codeshares = []
            for row3 in cur3:
                codeshare = row3['dup_flight_number']
                codeshares.append(codeshare)
            fp = FlightPeriod(fn, row['start_date'], row['end_date'], row['frequency_code'], spn,
                              row2['start_city'], int(row2['departure_time']),
                              row2['end_city'], int(row2['arrival_time']),
                              row2['aircraft'], codeshares)
            fperds.append(fp)

    return fperds


def ReadFlightPeriodsLatest(conn, flightNumber, dt1, dt2):

    printlog(1, "Flight periods (flight %s)" \
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
                % ( dt1.strftime("%m/%d/%Y") )
    if dt2 is not None:
        SpSql += \
            " AND end_date <= '%s'" \
                % ( dt2.strftime("%m/%d/%Y") )
    SpSql += \
        " GROUP BY flight_number"
    printlog(2, SpSql)
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
                % ( fn, end_date.strftime("%m/%d/%Y") )
        printlog(2, SpSql1)
        cur1.execute(SpSql1)
        for row1 in cur1:
            spn = int(row1['schedule_period_no'])
            printlog(1, "Flight %s start %s end %s frequency %s (schedule period %d)" % ( fn, row1['start_date'], end_date, row1['frequency_code'], spn), 1)
            SpSql2 = \
                "SELECT DISTINCT fps.aircraft_code aircraft, fsd.departure_airport start_city, fsd.arrival_airport end_city," \
                " departure_time, arrival_time" \
                " FROM flight_perd_segm fps, flight_segm_date fsd" \
                " WHERE fps.flight_number = '%s' AND fps.schedule_period_no = %d" \
                " AND fps.flight_number = fsd.flight_number" \
                " AND fps.schedule_period_no = fsd.schedule_period_no" \
                    % ( fn, spn )
            printlog(2, SpSql2)
            cur2.execute(SpSql2)
            for row2 in cur2:
                SpSql3 = \
                    "SELECT DISTINCT dup_flight_number FROM flight_shared_leg WHERE flight_number = '%s' AND schedule_period_no = %d" \
                        % ( fn, spn )
                printlog(2, SpSql3)
                cur3.execute(SpSql3)
                codeshares = []
                for row3 in cur3:
                    codeshare = row3['dup_flight_number']
                    codeshares.append(codeshare)
                fp = FlightPeriod(fn, row1['start_date'], row1['end_date'], row1['frequency_code'], spn,
                                row2['start_city'], int(row2['departure_time']),
                                row2['end_city'], int(row2['arrival_time']),
                                row2['aircraft'], codeshares)
                fperds.append(fp)

    return fperds


def isMarketingOrOperational(conn, flightNumber, dt1, dt2, frequency=None):

    startDate = dt1.strftime("%m/%d/%Y")
    endDate = dt2.strftime("%m/%d/%Y")
    SpSql = \
        "SELECT COUNT(*) mif" \
        " FROM flight_shared_leg fsl, city_pair cp, flight_segm_date fsd" \
        " WHERE fsl.dup_flight_number = '%s'" \
        "  AND fsl.flight_date BETWEEN '%s' AND '%s'" \
        "  AND fsl.departure_airport = cp.start_city" \
        "  AND fsl.arrival_airport = cp.end_city" \
        "  AND fsd.flight_number = fsl.dup_flight_number" \
        "  AND fsd.city_pair = cp.city_pair" \
        "  AND fsl.flight_date = fsd.flight_date" \
            % ( flightNumber, startDate, endDate)
    if frequency is not None:
        SpSql += \
            "  AND WEEKDAY(fsd.flight_date)::CHAR IN ('%s','%s','%s','%s','%s','%s','%s')" \
                % (frequency[0], frequency[1], frequency[2], frequency[3],
                   frequency[4], frequency[5], frequency[6] )
    printlog(2, SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)

    marketingInFlightSharedLeg =  None
    for row in cur:
        marketingInFlightSharedLeg = int(row['mif'])

    print "Found %d marketing flights for flight %s from %s to %s" \
        % (marketingInFlightSharedLeg, flightNumber, startDate, endDate)


def ReadConfigNumberOfSeats(conn, AircraftCode, haveClassCode=1, yClassCode='C', ClassCode='Y'):

    print "Read configuration for aircraft code %s [aircraft_config]" % AircraftCode
    #SpSql = \
        #"SELECT first 1 config_table_no, seat_capacity"
        #"  FROM aircraft_config"
        #"  WHERE aircraft_code = '%s'"
        #"  AND seat_capacity ="
        #"   ( SELECT MAX ( seat_capacity )"
        #"            FROM aircraft_config"
        #"           WHERE aircraft_code = '%s'"
        #"             AND selling_class = DECODE ( '%s', 0, '%s', '%s' ))"
    SpSql = \
        "SELECT config_table_no, seat_capacity" \
        "  FROM aircraft_config" \
        "  WHERE aircraft_code = '%s'" \
        "  AND seat_capacity =" \
        "   ( SELECT MAX ( seat_capacity )" \
        "            FROM aircraft_config" \
        "           WHERE aircraft_code = '%s')"  \
            % (AircraftCode, AircraftCode)

    printlog(2, SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)
    ConfigTableNo = 0
    NoOfSeats = 0
    n = 0
    for row in cur:
        ConfigTableNo = str(row['config_table_no'])
        NoOfSeats =  int(row['seat_capacity'] or 0)
        print "\t config table number %s seats %d" % (ConfigTableNo, NoOfSeats)
        n += 1

    if n == 0:
        print "\t not found"

    return ConfigTableNo, NoOfSeats


def CheckSchedPeriod(conn, dt1, dt2, alteredFrequency,
                    flightNumber, freqCode, newViacities, aircraftConfig):

    startDate = dt1.strftime("%m/%d/%Y")
    endDate = dt2.strftime("%m/%d/%Y")
    print "Check schedule period from %s to %s freq %s (%s) flight %s via %s aircraft %s [flight_periods]" \
        % (startDate, endDate, alteredFrequency, freqCode, flightNumber, \
           newViacities, aircraftConfig)

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
    printlog(2, SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)
    for row in cur:
        print "Freq %s period %3s status %s start %s end %s" \
            % (row['fc'], row['spn'], row['fss'], row['fps'], row['fpe'])


def ReadSchedPeriod(conn, dt1, dt2, alteredFrequency,
                    flightNumber, freqCode, newViacities, aircraftConfig):

    startDate = dt1.strftime("%m/%d/%Y")
    endDate = dt2.strftime("%m/%d/%Y")
    print "Read schedule period from %s to %s freq %s (alter %s) flight %s via %s aircraft %s [flight_periods, flight_segm_date, flight_perd_legs]" \
        % (startDate, endDate, freqCode, alteredFrequency, flightNumber, \
           newViacities, aircraftConfig)
    SpSql = \
         "SELECT FIRST 1 fsd.schedule_period_no spn" \
         " FROM flight_periods fp, flight_segm_date fsd, flight_perd_legs fpl" \
         "  GROUP BY fp.flight_number, fp.start_date,fp.end_date," \
         "   fp.frequency_code, fp.schedule_period_no," \
         "   fp.flgt_sched_status, fsd.flight_number," \
         "   fsd.flight_date, fsd.flgt_sched_status," \
         "   fsd.schedule_period_no, fp.via_cities," \
         "   fpl.flight_number , fpl.schedule_period_no," \
         "   fpl.config_table_no" \
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
         "   AND (SELECT COUNT(flight_date) FROM flight_segm_date WHERE flight_date BETWEEN '%s' AND '%s' AND flight_number = fp.flight_number ) = 0" \
         "   AND fp.end_date + 7 > '%s'" \
         "   AND (WEEKDAY('%s'))::CHAR IN('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
         "   AND fp.flgt_sched_status IN('A','S')" \
         "   AND fp.flight_number='%s'" \
         "   AND fp.frequency_code='%s'" \
         "   AND fp.via_cities='%s'" \
         "   AND fpl.config_table_no='%s'" \
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
    printlog(2, SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)
    n = 0
    for row in cur:
        print "\t schedule period %s" % row['spn']
        n += 1

    if n == 0:
        print "\t not found"

    return n


def DatesConsecutiveByFrequency(conn, flight_number, dt1, schedule_period_no):

    print "Dates for flight %s date %s period %s [flight_periods]" \
        % (flight_number, dt1, str(schedule_period_no))
    startDate = dt1.strftime("%m/%d/%Y")
    SpSql = \
        "SELECT WEEKDAY(end_date) ed, WEEKDAY('%s') sd" \
         " FROM flight_periods" \
         " WHERE flight_number='%s'" \
         " AND schedule_period_no=%d" \
         " AND flgt_sched_status IN ( 'A', 'S' )" \
             % (startDate, flight_number, schedule_period_no)
    printlog(2, SpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SpSql)
    for row in cur:
        print "\tStart %s end %s" % (row['sd'], row['ed'])


def GetFrequencies():
    SpSql = \
        "SELECT DISTINCT frequency_code, config_table_no                " \
        "  FROM flight_configuration                                    " \
        "WHERE ( ? LIKE flight_number OR                                " \
        "       flight_number LIKE DECODE ( ?, '', ?, ? ))    AND       " \
        "      (frequency_code [ 1, 1 ] =  DECODE ( ? , '-', '', ? ) OR " \
        "       frequency_code [ 2, 2 ] =  DECODE ( ? , '-', '', ? ) OR " \
        "       frequency_code [ 3, 3 ] =  DECODE ( ? , '-', '', ? ) OR " \
        "       frequency_code [ 4, 4 ] =  DECODE ( ? , '-', '', ? ) OR " \
        "       frequency_code [ 5, 5 ] =  DECODE ( ? , '-', '', ? ) OR " \
        "       frequency_code [ 6, 6 ] =  DECODE ( ? , '-', '', ? ) OR " \
        "       frequency_code [ 7, 7 ] =  DECODE ( ? , '-', '', ? ) OR " \
        "       frequency_code = '-------' ) "
