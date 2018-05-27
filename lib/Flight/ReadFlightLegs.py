# @file ReadFlightLegs.py


import sys
import psycopg2
from BarsLog import set_verbose, get_verbose, printlog
from ReadDateTime import ReadDate
from FlightData import FlightData


# Check flight date leg
def ReadFlightDateLegs(conn, flight_number, flight_date):

    flight_date_leg_ids = []
    print "Flight date legs for flight %s board %s [flight_date_leg]" % (flight_number, flight_date)
    RcSql = \
        "SELECT flight_date_leg_id,trim(flight_number) fn,board_date,departure_time," \
        " departure_airport,arrival_airport,leg_number,update_user,update_time" \
        " FROM flight_date_leg WHERE flight_number = '%s' AND board_date = '%s'"  \
        % (flight_number, flight_date.strftime("%m/%d/%Y"))
    printlog(RcSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        fli = int(row['flight_date_leg_id'] or 0)
        flight_date_leg_ids.append(fli)
        print "\tleg id %d flight %s date %s depart %s time %s arrive %s leg %d user %s update %s" \
            % (fli, str(row['fn'] or ''), row['board_date'], row['departure_airport'], \
               row['departure_time'],  # .isoformat().split("T")[1][0:5],
               row['arrival_airport'], row['leg_number'], \
               row['update_user'], row['update_time'])
        n += 1

    if n == 0:
        print "\t not found"

    return flight_date_leg_ids


def ReadFlightSharedLeg(conn, flight_number, dts):

    print "Flight shared legs for flight %s board %s [flight_shared_leg]" \
        % (flight_number, dts.strftime("%Y-%m-%d"))
    FslSql = \
        "select dup_flight_number,dup_board_date,dup_departure_airport,dup_arrival_airport,dup_flight_date," \
        "date_change_ind,flight_path_code,departure_terminal,arrival_terminal,config_table_no,aircraft_code,leg_number," \
        "update_user,update_time" \
        " FROM flight_shared_leg" \
        " WHERE flight_number='%s' AND board_date='%s'" \
            % (flight_number, dts.strftime("%m/%d/%Y"))
    printlog(FslSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(FslSql)
    config_table_no = None
    aircraft_codes = []
    config_table_nos = []
    n = 0
    for row in cur:
        print "\tdup %6s" % row['dup_flight_number'],
        print "board %s" % row['dup_board_date'],
        print "change %s" % row['date_change_ind'],
        print "path code %s" % row['flight_path_code'],
        #print "term %s" % row['departure_terminal'],
        #print "term %s" % row['arrival_terminal'],
        config_table_no = row['config_table_no']
        config_table_nos.append(config_table_no)
        print "config %s" % config_table_no,
        aircraft_code = str(row['aircraft_code'])
        print "aircraft %s" % aircraft_code,
        aircraft_codes.append(aircraft_code)
        print "leg %s" % row['leg_number'],
        print "user %s update %s" % (row['update_user'], row['update_time']),
        print
        n += 1

    if n == 0:
        print "\t not found"
    return aircraft_codes, config_table_nos


# Check test period leg
def ReadtestPeriodLegs(conn, flight_number, schedule_period_no):

    print "<TEST> Period legs for flight %s, schedule period %d [test_perd_legs]" \
        % (flight_number, schedule_period_no)
    RcSql = \
        "SELECT departure_time,arrival_time,departure_airport,arrival_airport," \
        "date_change_ind,config_table_no,flight_path_code,leg_number,update_time" \
        " FROM test_perd_legs" \
        " WHERE flight_number='%s' AND schedule_period_no=%d" \
        % (flight_number, schedule_period_no)
    printlog(RcSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(RcSql)
    n = 0
    for row in cur:
        print "\tdepart %s time %s arrive %s time %s change %d config %s path %s leg %d update %s" \
            % (row['departure_airport'], row['departure_time'],
               row['arrival_airport'], row['arrival_time'],
               row['date_change_ind'], row['config_table_no'],
               row['flight_path_code'], row['leg_number'], row['update_time'])
        n += 1

    if n == 0:
        print "\t not found"
    #print
    return


# Read table asr_reconcile_history
def ReadAsrReconcileHistory(conn, flight_date_leg_id):

    print "ASR reconcile history for flight date leg ID %d [asr_reconcile_history]" \
        % flight_date_leg_id

    RcSql = \
        "SELECT action_id,action_detail,update_user,update_time" \
        " FROM asr_reconcile_history" \
        " WHERE flight_date_leg_id=%d" % flight_date_leg_id
    printlog(RcSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(RcSql)
    n = 0
    for row in cur:
        print "\tID %8d : %s user %s update %s" \
            % (row['action_id'],
               row['action_detail'], row['update_user'], row['update_time'])
        n += 1

    if n == 0:
        print "\tnot found"

    return
