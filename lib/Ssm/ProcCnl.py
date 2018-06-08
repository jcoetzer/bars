# @file ProcCnl.py
#
"""
Process cancellation of flights.
"""

import sys
import ply.lex as lex
import ply.yacc as yacc
import datetime

from Ssm.SsmData import SsmData, read_ssm_data
from BarsLog import printlog, set_verbose
from ReadDateTime import ReadDate, DateRange
from Ssm.SsmDb import CheckFlightPeriod, GetCityPair


def DeleteSellingClasses(conn,
                         pflight_number,
                         flight_date):

    ssmSql = "DELETE FROM selling_classes" \
            " WHERE flight_date_id IN (" \
            " SELECT flight_date_id FROM flight_dates" \
                " WHERE flight_number='%s' and depart_date='%s')" \
                    % (pflight_number, flight_date)
    printlog(2, "%s" % ssmSql)
    cur = conn.cursor()
    cur.execute(ssmSql)
    rowcount = cur.rowcount
    printlog(2, "Deleted %d row(s)" % rowcount)
    cur.close()
    return rowcount


def DeleteFlightDate(conn,
                     pflight_number,
                     flight_date):
    ssmSql = "DELETE FROM flight_dates" \
             " WHERE flight_number='%s' and depart_date='%s'" \
                 % (pflight_number, flight_date.strftime("%Y-%m-%d"))
    printlog(2, "%s" % ssmSql)
    cur = conn.cursor()
    cur.execute(ssmSql)
    rowcount = cur.rowcount
    printlog(2, "Deleted %d row(s)" % rowcount)
    cur.close()
    return rowcount


def DeleteInventrySegment(conn,
                          pflight_number,
                          flight_date):
    ssmSql = "DELETE FROM inventry_segment" \
             " WHERE flight_number='%s' and flight_date='%s'" \
                 % (pflight_number, flight_date.strftime("%Y-%m-%d"))
    printlog(2, "%s" % ssmSql)
    cur = conn.cursor()
    cur.execute(ssmSql)
    rowcount = cur.rowcount
    printlog(2, "Deleted %d row(s)" % rowcount)
    cur.close()
    return rowcount


def DeleteFlightPeriod(conn,
                       pflight_number,
                       pschedule_period_no):
    cur = conn.cursor()

    dfpSql = "DELETE FROM flt_perd_seg_cls " \
             "WHERE flight_number = '%s' AND schedule_period_no = %d" % (pflight_number, pschedule_period_no)
    printlog(2, "%s" % dfpSql)
    cur.execute(dfpSql)
    rowcount = cur.rowcount
    printlog(2, "Deleted %d row(s)" % rowcount)

    dfpSql = "DELETE FROM flight_perd_cls " \
             "WHERE flight_number = '%s' AND schedule_period_no = %d" % (pflight_number, pschedule_period_no)
    printlog(2, "%s" % dfpSql)
    cur.execute(dfpSql)
    rowcount = cur.rowcount
    printlog(2, "Deleted %d row(s)" % rowcount)

    dfpSql = "DELETE FROM flight_perd_prnt " \
             "WHERE flight_number = '%s' AND schedule_period_no = %d" % (pflight_number, pschedule_period_no)
    printlog(2, "%s" % dfpSql)
    cur.execute(dfpSql)
    rowcount = cur.rowcount
    printlog(2, "Deleted %d row(s)" % rowcount)

    dfpSql = "DELETE FROM flight_perd_segm " \
             "WHERE flight_number = '%s' AND schedule_period_no = %d" % (pflight_number, pschedule_period_no)
    printlog(2, "%s" % dfpSql)
    cur.execute(dfpSql)
    rowcount = cur.rowcount
    printlog(2, "Deleted %d row(s)" % rowcount)

    dfpSql = "DELETE FROM flight_perd_legs " \
             "WHERE flight_number = '%s' AND schedule_period_no = %d" % (pflight_number, pschedule_period_no)
    printlog(2, "%s" % dfpSql)
    cur.execute(dfpSql)
    rowcount = cur.rowcount
    printlog(2, "Deleted %d row(s)" % rowcount)

    dfpSql = "DELETE FROM flight_periods " \
             "WHERE flight_number = '%s' AND schedule_period_no = %d" % (pflight_number, pschedule_period_no)
    printlog(2, "%s" % dfpSql)
    cur.execute(dfpSql)
    rowcount = cur.rowcount
    printlog(2, "Deleted %d row(s)" % rowcount)
    cur.close()
    return rowcount


def DeleteFlightInfo(conn,
                    flight,
                    boardDate):
    cur = conn.cursor()
    fiSql = "DELETE FROM flight_information " \
            "WHERE flight_number='%s' AND board_date='%s'" \
            % (flight, boardDate.strftime("%Y-%m-%d"))
    printlog(2,fiSql)
    cur.execute(fiSql)

    rowcount = cur.rowcount
    printlog(2, "Deleted %d row(s)" % rowcount)
    cur.close()
    return rowcount


def DeleteFlightSegmDate(conn,
                         aflight_number,
                         acity_pair,
                         aflight_date):

    cur = conn.cursor()
    FsdSql = \
        "DELETE FROM flight_segm_date WHERE flight_number = '%s' AND flight_date = '%s'" \
            % (aflight_number, aflight_date)
    if acity_pair != 0:
        FsdSql += \
            " AND city_pair = %d" % acity_pair
    printlog(2,FsdSql)
    cur.execute(FsdSql)
    rowcount = cur.rowcount
    printlog(2, "Deleted %d row(s)" % rowcount)
    cur.close()
    return rowcount


def ProcCnl(conn,
            ssm):

    printlog(2, "Cancel flight %s" % ssm.flight_number)
    #city_pair_id = GetCityPair(conn,
                               #ssm.departure_airport,
                               #ssm.arrival_airport)
    #if city_pair_id == 0:
        #print "City pair %s and %s does not exist" % (ssm.departure_airport, ssm.arrival_airport)
        #return -1
    city_pair_id = 0

    flight_period_id, sdate, edate = CheckFlightPeriod(conn, ssm)
    if flight_period_id == 0:
        printlog(0, "Flight period for %s does not exist" % ssm.flight_number)
        #return -1

    if sdate != ssm.start_date:
        printlog(0, "Start date from input %s does not match stored value %s"
            % (ssm.start_date, sdate))
    elif edate != ssm.end_date:
        printlog(0, "End date from input %s does not match stored value %s"
            % (ssm.end_date, edate))
    else:
        pass

    #DeleteFlightPeriod(conn, ssm.flight_number, flight_period_id)

    #freq = str(ssm.frequency_code)
    #for flight_date in DateRange(ssm.start_date, ssm.end_date):
        #fday = str(flight_date.strftime('%w'))
        #if fday == '0':
            #fday = '7'
        #if fday in freq:
            #printlog(2, "Delete flight date %s (day %s)" % (flight_date, fday))
            ##DeleteSellingClasses(conn, ssm, flight_date)
            #DeleteFlightDate(conn, ssm.flight_number, flight_date)

    ssmdates = []
    cdate = ssm.start_date
    while cdate <= ssm.end_date:
        wday = cdate.weekday()+1
        printlog(2, "Date %s (day %d)" % (cdate.strftime("%Y-%m-%d"), wday))
        if wday in ssm.frequency_codes:
            ssmdates.append(cdate)
        cdate += datetime.timedelta(days=1)

    for flight_date in ssmdates:
        printlog(2, "Delete flight date %s (day %s)" % (flight_date, flight_date))
        #DeleteSellingClasses(conn, ssm, flight_date)
        #DeleteFlightDate(conn, ssm.flight_number, flight_date)
        DeleteFlightInfo(conn, ssm.flight_number, flight_date)
        DeleteFlightSegmDate(conn, ssm.flight_number, city_pair_id, flight_date)
        DeleteInventrySegment(conn, ssm.flight_number, flight_date)

    if flight_period_id != 0:
        DeleteFlightPeriod(conn, ssm.flight_number, flight_period_id)

