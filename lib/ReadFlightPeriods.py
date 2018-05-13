#!/usr/bin/python -B
#
# @file ReadFlightPeriods.py
#

import sys
import getopt
import psycopg2
from datetime import datetime, timedelta, datetime
from BarsLog import set_verbose, printlog
from ReadDateTime import ReadDate


# Read flight periods as needed by GUI
def ReadFlightPeriodsGui(conn, flight_number, schd_perd_no):

    print "Flight periods for flight %d, schedule period %d [flight_periods,test_periods]" \
        % (flight_number, schd_perd_no)
    AdSql = \
        "SELECT 2 AS CONST, COUNT(*) AS c, flgt_sched_status FROM flight_periods " \
        " WHERE flight_number = '%s' AND flgt_sched_status NOT IN ('A','S','T') AND schd_perd_no = %d GROUP BY 3" \
        " UNION SELECT 3 AS CONST, COUNT(*) AS c, chng_category FROM test_periods "\
        "  WHERE flight_number = '%s' AND schd_perd_no = %d AND Authority_Level > 9999 GROUP BY 3" \
        " UNION SELECT 4 AS CONST, COUNT(*) AS c, user_name FROM test_periods " \
        "  WHERE flight_number = '%s' AND schd_perd_no = %d AND Scrutiny_Flg = 'Y' GROUP BY 3" \
        " UNION SELECT 5 AS CONST, COUNT(*) AS c, chng_category FROM test_periods " \
        "  WHERE flight_number = '%s' AND schd_perd_no = %d GROUP BY 3 ORDER BY 1" \
            % (flight_number, schd_perd_no, flight_number, schd_perd_no,
               flight_number, schd_perd_no, flight_number, schd_perd_no)
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AdSql)
    n = 0
    for row in cur:
        n += 1
        print "count %s status %s" % (row['c'], row['flgt_sched_status'])
    if n == 0:
        print "\tnot found"


# Read table flight_periods
def ReadFlightPeriods(conn, flight_number, schd_perd_no=None):

    print "Flight periods for flight %s [flight_periods]" % flight_number,
    AdSql= \
	    "SELECT flight_number,start_date,end_date,frequency_code,schd_perd_no,invt_end_date,control_branch,invt_control_flg," \
	    " wait_lst_ctrl_flg,via_cities,flgt_sched_status,open_end_flg,scrutiny_flg,gen_flag_invt,user_name,user_group," \
            " update_time" \
	    " FROM flight_periods WHERE flight_number = '%s'" % flight_number
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print

    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tflight %6s start %10s end %10s sched %5d via %7s wait %4s sched %4s flag %4s end %10s user %s update %s" \
            % (row['flight_number'], row['start_date'], row['end_date'], int(row['schd_perd_no']), row['via_cities'], \
               row['wait_lst_ctrl_flg'], \
               row['flgt_sched_status'], row['gen_flag_invt'], row['invt_end_date'], row['user_name'], row['update_time'])
    if n == 0:
        print "\tnot found"


# Read table flight_periods
def ReadFlightPeriodsDate(conn, flight_number, dts):

    print "Flight periods for flight %s board date %s [flight_periods]" \
        % (flight_number, dts.strftime("%Y-%m-%d"))
    flight_date = dts.strftime("%m/%d/%Y")
    # Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.
    flight_dow = int(dts.strftime("%w"))
    # Convert to Monday=1, Sunday=7
    if flight_dow == 0:
        flight_dow = 7

    AdSql= \
        "SELECT flight_number,start_date,end_date,frequency_code," \
        "schd_perd_no,invt_end_date,control_branch,invt_control_flg," \
        "wait_lst_ctrl_flg,via_cities,flgt_sched_status,open_end_flg," \
        "scrutiny_flg,gen_flag_invt,user_name,user_group," \
        "update_time" \
        " FROM flight_periods" \
        " WHERE flight_number = '%s' AND start_date<='%s' AND end_date>='%s'" \
        " AND frequency_code LIKE '%%%d%%'" \
        % (flight_number, flight_date, flight_date, flight_dow)
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AdSql)
    rvals = []
    n = 0
    for row in cur:
        n += 1
        rval = int(row['schd_perd_no'])
        rvals.append(rval)
        print "\tflight %6s start %10s end %10s sched %5d frequency %7s" \
              " via %7s wait %4s status %4s inventory %4s end %10s user %s update %s" % \
            (row['flight_number'], row['start_date'], row['end_date'],
             rval, row['frequency_code'], row['via_cities'],
             row['wait_lst_ctrl_flg'], row['flgt_sched_status'],
             row['gen_flag_invt'], row['invt_end_date'], row['user_name'], row['update_time'])
    if n == 0:
        print "\tnot found"

    return rvals


# Read table test_periods
def ReadTestPeriods(conn, flight_number, schd_perd_no=None, dts=None):

    print "<TEST> Periods for flight %s [test_periods]" % flight_number,
    AdSql = \
        "SELECT flgt_sched_status,chng_category,user_name," \
        "chng_category,schd_perd_no,user_name,update_time" \
        " FROM test_periods" \
        " WHERE flight_number = '%s'" % flight_number
    if dts is not None:
        print "board %s" % dts.strftime("%Y-%m-%d"),
        flight_date = dts.strftime("%m/%d/%Y")
        AdSql += \
            " and start_date<='%s' and end_date>='%s'" \
                % (flight_date, flight_date)
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tstatus %s change %s user %s sched %d user %s update %s" \
            % (row['flgt_sched_status'], row['chng_category'],
               row['user_name'], int(row['schd_perd_no']), row['user_name'], row['update_time'])
    if n == 0:
        print "\tnot found"


# Read table test_inventry_segm
def ReadTestInventrySegm(conn, flight_number, schd_perd_no=None,
                         selling_cls_code=None):

    print "<TEST> Inventory segment for flight %s [test_inventry_segm]" % flight_number,
    AdSql = \
        "SELECT flight_date,city_pair_no,selling_cls_code,departure_city," \
        "arrival_city,leg_number,segment_number,seat_capacity,user_name,update_time" \
        " FROM test_inventry_segm" \
        " WHERE flight_number = '%s'" \
        % flight_number
    if selling_cls_code is not None:
        print ", selling class %s" % selling_cls_code,
        AdSql += \
            " AND selling_cls_code = '%s'" % selling_cls_code
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute("\n%s"% AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tclass %s city pair %s date %s depart %s arrive %s leg %s segment %s capacity %s user %s update %s" \
            % (row['selling_cls_code'], row['city_pair_no'], row['flight_date'], row['departure_city'], \
               row['arrival_city'], \
               row['leg_number'], row['segment_number'], row['seat_capacity'], row['user_name'], row['update_time'])
    if n == 0:
        print "\tnot found"


def ReadFlightPerdLegs(conn, flight_number, schd_perd_no=None):

    print "Flight period legs for flight %s [flight_perd_legs]" % flight_number,
    AdSql = \
        "SELECT depr_airport,arrv_airport," \
        "departure_time departure," \
        "arrival_time arrival," \
        "date_change_ind,config_table_no,flight_path_code,depr_terminal_no," \
        "arrv_terminal_no,leg_number,update_time" \
        " FROM flight_perd_legs" \
        " WHERE flight_number = '%s'" \
        % flight_number
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute("\n%s"% AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tdepart %4s time %5s arrive %4s time %5s update %s" \
            % (row['depr_airport'], row['departure'], row['arrv_airport'],
               row['arrival'], row['update_time'])
    if n == 0:
        print "\tnot found"


# Read table flight_perd_segm
def ReadFlightPerdSegm(conn, flight_number, schd_perd_no=None):

    print "Flight period segment for flight %s [flight_perd_segm]" % flight_number,
    AdSql = \
        "SELECT city_pair_no,post_control_flg,aircraft_code," \
        "flight_closed_flg,flight_brdng_flg,segment_number,update_time" \
        " FROM flight_perd_segm" \
        " WHERE flight_number = '%s'" \
        % flight_number
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute("\n%s"% AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tcity pair %s post %s aircraft %s closed %s boarding %s" \
              "segment %s update %s" \
            % (row['city_pair_no'], row['post_control_flg'],
               row['aircraft_code'], row['flight_closed_flg'], \
               row['flight_brdng_flg'], row['segment_number'], row['update_time'])
    if n == 0:
        print "\tnot found"


# Read table test_perd_segm
def ReadTestPerdSegm(conn, flight_number, schd_perd_no=None):

    print "<TEST> flight period segment for flight %s [test_perd_segm]" % flight_number,
    AdSql = \
        "SELECT city_pair_no,post_control_flg,aircraft_code," \
        "flight_closed_flg,flight_brdng_flg,segment_number,update_time" \
        " FROM test_perd_segm" \
        " WHERE flight_number = '%s'" \
        % flight_number
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute("\n%s"% AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tcity pair %s post %s aircraft %s closed %s boarding %s" \
              "segment %s update %s" \
            % (row['city_pair_no'], row['post_control_flg'],
               row['aircraft_code'], row['flight_closed_flg'], \
               row['flight_brdng_flg'], row['segment_number'], row['update_time'])
    if n == 0:
        print "\tnot found"


# Read table flight_perd_cls
def ReadFlightPerdCls(conn, flight_number, schd_perd_no=None,
                         selling_cls_code=None):

    print "Flight period class for flight %s [flight_perd_cls]" % flight_number,
    AdSql = \
        "select flight_number,schd_perd_no,selling_cls_code," \
        "TRIM(parent_sell_cls) parent,display_priority,update_time" \
        " FROM flight_perd_cls WHERE flight_number = '%s'" \
        % flight_number
    if selling_cls_code is not None:
        print ", selling class %s" % selling_cls_code,
        AdSql += \
            " AND selling_cls_code = '%s'" % selling_cls_code
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tclass %s parent class %s priority %s update %s" \
            % (row['selling_cls_code'], row['parent'], row['display_priority'], row['update_time'])
    if n == 0:
        print "\tnot found"


# Read table test_perd_cls
def ReadTestPerdCls(conn, flight_number, schd_perd_no=None,
                    selling_cls_code=None):

    print "<TEST> Flight period class for flight %s [test_perd_cls]" % flight_number,
    AdSql = \
        "select flight_number,schd_perd_no,selling_cls_code," \
        "TRIM(parent_sell_cls) parent,display_priority,update_time" \
        " FROM test_perd_cls WHERE flight_number = '%s'" \
        % flight_number
    if selling_cls_code is not None:
        print ", selling class %s" % selling_cls_code,
        AdSql += \
            " AND selling_cls_code = '%s'" % selling_cls_code
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tclass %s parent class %s priority %s update %s" \
            % (row['selling_cls_code'], row['parent'], row['display_priority'], row['update_time'])
    if n == 0:
        print "\tnot found"


# Read table flt_perd_seg_cls
def ReadFlightPerdSegCls(conn, flight_number, schd_perd_no=None,
                             selling_cls_code=None):

    print "Flight period segment class for flight %s [flt_perd_seg_cls]" % flight_number,
    AdSql = \
        "SELECT city_pair_no,selling_cls_code,segment_number,update_time " \
        "FROM flt_perd_seg_cls WHERE flight_number = '%s'" \
        % flight_number
    if selling_cls_code is not None:
        print ", selling class %s" % selling_cls_code,
        AdSql += \
            " AND selling_cls_code = '%s'" % selling_cls_code
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tclass %s city pair %s segment %s update %s" \
            % (row['selling_cls_code'], row['city_pair_no'],
               row['segment_number'], row['update_time'])
    if n == 0:
        print "\tnot found"


# Read table flight_perd_prnt
def ReadFlightPerdPrnt(conn, flight_number, schd_perd_no=None,
                          selling_cls_code=None):

    print "Flight period parent for flight %s [flight_perd_prnt]" % flight_number,
    AdSql = \
        "select selling_cls_code,parent_sell_cls,update_time " \
        " FROM flight_perd_prnt WHERE flight_number = '%s'" \
        % flight_number
    if selling_cls_code is not None:
        print ", selling class %s" % selling_cls_code,
        AdSql += \
            " AND selling_cls_code = '%s'" % selling_cls_code
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tclass %s parent class %s update %s" \
            % (row['selling_cls_code'], row['parent_sell_cls'], row['update_time'])
    if n == 0:
        print "\tnot found"


# Read table test_perd_prnt
def ReadTestPerdPrnt(conn, flight_number, schd_perd_no=None,
                          selling_cls_code=None):

    print "<TEST> Flight period parent for flight %s [test_perd_prnt]" % flight_number,
    AdSql = \
        "select selling_cls_code,parent_sell_cls,update_time " \
        " FROM test_perd_prnt WHERE flight_number = '%s'" \
        % flight_number
    if selling_cls_code is not None:
        print ", selling class %s" % selling_cls_code,
        AdSql += \
            " AND selling_cls_code = '%s'" % selling_cls_code
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tclass %s parent class %s update %s" \
            % (row['selling_cls_code'], row['parent_sell_cls'], row['update_time'])
    if n == 0:
        print "\tnot found"


# Read table inventry_realloc
def read_inventry_realloc(conn, flight_number, schd_perd_no=None,
                          selling_cls_code=None):

    print "Inventory reallocation for flight %s [inventry_realloc]" % flight_number,
    AdSql = \
        "select flight_date,city_pair_no,selling_cls_code,start_date," \
        "end_date,frequency_code,crea_user_code,update_time " \
        " FROM inventry_realloc WHERE flight_number = '%s'" \
        % flight_number
    if selling_cls_code is not None:
        print ", selling class %s" % selling_cls_code,
        AdSql += \
            " AND selling_cls_code = '%s'" % selling_cls_code
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tclass %s city pair %s date %s start %s end %s frequency %s user %s update %s" \
            % (row['selling_cls_code'], row['city_pair_no'],
               row['flight_date'], row['start_date'], row['end_date'],
               row['frequency_code'], row['crea_user_code'], row['update_time'])
    if n == 0:
        print "\tnot found"


# Read table schd_chng_action
def ReadSchdChngAction(conn, flight_number, schd_perd_no=None,
                          selling_cls_code=None):

    print "Schedule change action for flight %s [schd_chng_action]" % flight_number,
    AdSql = \
        "select city_pair_no,selling_cls_code,depr_airport,arrv_airport," \
        "segm_update_flg,seg_cls_updt_flg,action_date,action_type," \
        "processing_flg,update_time " \
        " FROM schd_chng_action WHERE flight_number = '%s'" \
        % flight_number
    if selling_cls_code is not None:
        print ", selling class %s" % selling_cls_code,
        AdSql += \
            " AND selling_cls_code = '%s'" % selling_cls_code
    if schd_perd_no is not None:
        print ", schedule period %d" % schd_perd_no,
        AdSql += \
            " AND schd_perd_no = %d" % schd_perd_no
    print
    printlog(2, AdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AdSql)
    n = 0
    for row in cur:
        n += 1
        print "\tclass %s city pair %s depart %s arrive %s segment flag %s" \
              "class flag %s action %s process %s update %s" \
            % (row['selling_cls_code'], row['city_pair_no'],
               row['depr_airport'], row['arrv_airport'],
               row['segm_update_flg'], row['seg_cls_updt_flg'],
               row['action_date'], row['processing_flg'], row['update_time'])
    if n == 0:
        print "\tnot found"


