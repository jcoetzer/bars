# @file ReadSsmData.py

import sys
import psycopg2
from BarsLog import printlog
from ReadFlightPeriods import ReadFlightPeriods, ReadFlightPerdLegs
from ReadFlights import CheckFlight

def ReadSsmFlightData(conn, flight, end_date):

    print "Flight %s board %s data for SSM" \
        % (flight.flight_number, flight.board_date_iso)
    FbSql = \
        "SELECT DISTINCT fpl.depr_airport da,fpl.arrv_airport aa," \
        "fp.start_date sd,fp.end_date ed," \
        "fpl.schd_perd_no spn, fpl.leg_number ln,fp.via_cities vc," \
        "fp.flgt_sched_status fss," \
        "fp.frequency_code fc,fpl.departure_time dt, fpl.arrival_time at," \
        "fsd.aircraft_code acn,fpl.config_table_no ctn,fpl.depr_terminal_no dtn," \
        "fpl.arrv_terminal_no atn" \
        " FROM flight_perd_legs fpl, flight_periods fp,flight_segm_date fsd, aircraft_config ac" \
        " WHERE fpl.flight_number='%s'" \
            % (flight.flight_number)

    if len(flight.departure_airport):
        FbSql += " AND fpl.depr_airport='%s'" % flight.departure_airport
    if len(flight.arrival_airport):
        FbSql += " AND fpl.arrv_airport='%s'" % flight.arrival_airport

    if end_date.strftime("%m/%d/%Y")!=flight.board_date_mdy:
        FbSql += " AND fsd.flight_date BETWEEN '%s' AND '%s'" \
            % (flight.board_date_mdy, end_date.strftime("%m/%d/%Y"))
    else:
        FbSql += " AND fsd.flight_date='%s'" % flight.board_date_mdy

    FbSql += \
        " AND fpl.leg_number>=0" \
        " AND fp.flgt_sched_status IN ('A', 'R', 'D', 'M', 'U')" \
        " AND fp.flight_number=fpl.flight_number"  \
        " AND fsd.flight_number=fpl.flight_number" \
        " AND fsd.schd_perd_no=fpl.schd_perd_no"  \
        " AND fp.schd_perd_no=fpl.schd_perd_no" \
        " AND fpl.leg_number=fsd.leg_number" \
        " AND fsd.depr_airport=fpl.depr_airport" \
        " AND fsd.arrv_airport=fpl.arrv_airport" \
        " AND ac.aircraft_code=fsd.aircraft_code" \
        " AND ac.config_table_no=fpl.config_table_no" \
        " AND fp.frequency_code LIKE '%%%d%%'" \
        " ORDER BY fp.start_date, fpl.schd_perd_no, fpl.leg_number" \
            % flight.board_weekday

    printlog(2, FbSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FbSql)
    n = 0
    for row in cur:
        print "\t depart %s arrive %s start %s end %s sched %s leg %s via %s" \
              " status %s freq %s aircraft %s config %s" \
            % (row['da'], row['aa'], row['sd'], row['ed'], row['spn'],
               row['ln'], row['vc'], row['fss'], row['fc'], row['acn'],
               row['ctn'])
        n += 1

    if n == 0:
        print "\t not found"

    return n

def ReadSsmFlightData2(conn, flight, end_date):

    print "Flight %s board %s data for SSM" \
        % (flight.flight_number, flight.board_date_iso)
    FbSql = \
        "SELECT DISTINCT fpl.depr_airport da,fpl.arrv_airport aa," \
        "fp.start_date sd,fp.end_date ed," \
        "fpl.schd_perd_no spn, fpl.leg_number ln,fp.via_cities vc," \
        "fp.flgt_sched_status fss," \
        "fp.frequency_code fc,fpl.departure_time dt, fpl.arrival_time at," \
        "fsd.aircraft_code acn,fpl.config_table_no ctn,fpl.depr_terminal_no dtn," \
        "fpl.arrv_terminal_no atn" \
        " FROM flight_perd_legs fpl, flight_periods fp,flight_segm_date fsd, aircraft_config ac" \
        " WHERE fpl.flight_number='%s'" \
        " AND fpl.depr_airport='%s'" \
        " AND fpl.arrv_airport='%s'" \
        " AND fsd.flight_date BETWEEN '%s' AND '%s'" \
        " AND fpl.leg_number>=0" \
        " AND fp.flgt_sched_status IN ('A', 'R', 'D', 'M', 'U')" \
        " AND fp.flight_number=fpl.flight_number"  \
        " AND fsd.flight_number=fpl.flight_number" \
        " AND fsd.schd_perd_no=fpl.schd_perd_no"  \
        " AND fp.schd_perd_no=fpl.schd_perd_no" \
        " AND fpl.leg_number=fsd.leg_number" \
        " AND fsd.depr_airport=fpl.depr_airport" \
        " AND fsd.arrv_airport=fpl.arrv_airport" \
        " AND ac.aircraft_code=fsd.aircraft_code" \
        " AND ac.config_table_no=fpl.config_table_no" \
        " AND fp.frequency_code LIKE '%%%d%%'" \
        " ORDER BY fp.start_date, fpl.schd_perd_no, fpl.leg_number" \
        % (flight.flight_number, flight.departure_airport,
           flight.arrival_airport, flight.board_date_mdy,
           flight.board_date_mdy, flight.board_weekday)
    printlog(2, FbSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(FbSql)
    n = 0
    for row in cur:
        print "\t depart %s arrive %s start %s end %s sched %s leg %s via %s" \
              " status %s freq %s aircraft %s config %s" \
            % (row['da'], row['aa'], row['sd'], row['ed'], row['spn'],
               row['ln'], row['vc'], row['fss'], row['fc'], row['acn'],
               row['ctn'])
        n += 1

    if n == 0:
        print "\t not found"

    return n


def ReadSsmBookData(conn, flight, schedPerdNo):

    print "Flight %s schedule period %s bookings for SSM" \
        % (flight.flight_number, schedPerdNo)
    FbSql = \
        "SELECT DISTINCT i.book_no bn" \
        " FROM itenary i, action_codes ac, flight_periods fp, city_pair cp," \
        " flight_date_leg fdl, book b" \
        " WHERE fdl.flight_date between fp.start_date AND fp.end_date" \
        " AND i.itenary_stat_flag = 'A'" \
        " AND i.itenary_type = 'R'" \
        " AND i.route_no < 100" \
        " AND ac.action_code = i.reserve_status [ 1, 2 ]" \
        " AND ac.seat_rqst_type IN ('C', 'W', 'R')" \
        " AND fp.flight_number = i.flight_number" \
        " AND fdl.flight_number = i.flight_number" \
        " AND REPLACE( fp.frequency_code, '7', '0' ) LIKE '%%' || WEEKDAY(fdl.flight_date)::CHAR || '%%'" \
        " AND fdl.board_date = i.flight_date" \
        " AND i.city_pair_no = cp.city_pair_no" \
        " AND fdl.origin_airport_code = cp.start_city" \
        " AND fdl.destination_airport_code = cp.end_city" \
        " AND i.book_no = b.book_no" \
        " AND b.booking_status <> 'X'" \
        " AND flgt_sched_status = 'A'" \
        " AND fp.flight_number = '%s'" \
        " AND fp.schd_perd_no = %d" \
            % (flight.flight_number, schedPerdNo)
    printlog(2, FbSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FbSql)
    n = 0
    for row in cur:
        print "\t %d" % row['bn']
        n += 1

    if n == 0:
        print "\t not found"

    return n


def ReadAbsoluteRange(conn, flight):

    print "Absolute range for flight %s" % flight.flight_number
    FbSql = \
        "SELECT DISTINCT MIN(fpa.start_date) sd, MAX(fpb.end_date) ed, COUNT(*) cnt" \
        " FROM flight_perd_legs fpl, flight_periods fpa, flight_periods fpb, flight_segm_date fsd" \
        " WHERE fpl.flight_number = '%s'" \
        " AND fpl.leg_number >= 0" \
        " AND fpa.flgt_sched_status IN ('S', 'A', 'R', 'D', 'M', 'U')" \
        " AND fpa.flight_number = fpl.flight_number" \
        " AND fsd.flight_number = fpl.flight_number" \
        " AND fsd.schd_perd_no = fpl.schd_perd_no" \
        " AND fpa.schd_perd_no = fpl.schd_perd_no" \
        " AND fpa.schd_perd_no = fpb.schd_perd_no" \
        " AND fpa.flgt_sched_status = fpb.flgt_sched_status" \
        " AND fpa.schd_perd_no = fpb.schd_perd_no" \
        " AND fpa.flight_number = fpb.flight_number" \
            % flight.flight_number
    printlog(2, FbSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FbSql)
    n = 0
    sd = None
    ed = None
    cnt = 0
    for row in cur:
        sd = str(row['sd'] or '')
        ed = str(row['sd'] or '')
        cnt = int(row['cnt'] or 0)
        print "Start %s end %s count %d" %(row['sd'], row['ed'], row['cnt'])

    return cnt, sd, ed


def ReadSsmTim(conn, flight, sdate, edate, frequency_code):

    ReadAbsoluteRange(conn, flight)

    print "TIM data for flight %s from %s to %s" \
        % (flight.flight_number, sdate.strftime("%Y-%m-%d"), edate.strftime("%Y-%m-%d"))

    FbSql = \
        "SELECT DISTINCT fpl.depr_airport depr, fpl.arrv_airport arrv, fp.start_date sd, fp.end_date ed, fpl.schd_perd_no spn, " \
        "fpl.leg_number ln, fp.via_cities vc, fp.flgt_sched_status fss, fp.frequency_code fc," \
        "fpl.departure_time dt, fpl.arrival_time at, fsd.aircraft_code acd, fpl.config_table_no ctn," \
        "fpl.depr_terminal_no dtn, fpl.arrv_terminal_no atn" \
        " FROM flight_perd_legs fpl, flight_periods fp,flight_segm_date fsd, aircraft_config ac" \
        " WHERE fpl.flight_number = '%s'" \
        " AND fpl.depr_airport  = '%s'" \
        " AND fpl.arrv_airport  = '%s'" \
        " AND fsd.flight_date BETWEEN '%s' AND '%s' " \
        " AND fpl.leg_number >= 0" \
        " AND fp.flgt_sched_status IN ('A', 'R', 'D', 'M', 'U')" \
        " AND fp.flight_number = fpl.flight_number" \
        " AND fsd.flight_number = fpl.flight_number" \
        " AND fsd.schd_perd_no = fpl.schd_perd_no" \
        " AND fp.schd_perd_no = fpl.schd_perd_no" \
        " AND fpl.leg_number = fsd.leg_number" \
        " AND fsd.depr_airport = fpl.depr_airport" \
        " AND fsd.arrv_airport = fpl.arrv_airport" \
        " AND ac.aircraft_code = fsd.aircraft_code" \
        " AND ac.config_table_no = fpl.config_table_no" \
            % (flight.flight_number, flight.departure_airport, flight.arrival_airport,
               sdate.strftime("%m/%d/%Y"), edate.strftime("%m/%d/%Y"))
    if frequency_code is not None:
        FbSql += \
            " AND fp.frequency_code LIKE '%s'" % frequency_code.replace("-", "_")
    FbSql += \
        " ORDER BY fp.start_date, fpl.schd_perd_no, fpl.leg_number"
    printlog(2, FbSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FbSql)
    n = 0
    for row in cur:
        print "\t leg %d sched period %d status %s start %s end %s aircraft code %s config table %s frequency %s" \
            % (row['ln'], row['spn'], row['fss'], row['sd'], row['ed'], row['acd'], row['ctn'], row['fc'])
        n += 1

    if n == 0:
        print "\t not found"

    return n


def GetFlightDataSsm(conn, flight, sdate, edate, frequency_code):

    print "Flight %s schedule period %s bookings for SSM frequency %s" \
        % (flight.flight_number, schedPerdNo, frequency_code)
    FbSql = \
        """
        SELECT DISTINCT fpl.schd_perd_no spn, fpl.depr_airport da, fpl.arrv_airport aa, fp.start_date sd, fp.end_date ed, fpl.leg_number ln,
            fp.via_cities vc, fp.flgt_sched_status fss, fp.frequency_code fc, fpl.departure_time dt, fpl.arrival_time at, fps.aircraft_code ac,
            fpl.config_table_no ctn, fpl.depr_terminal_no dtn, fpl.arrv_terminal_no atn
        FROM flight_perd_legs fpl, flight_periods fp,flight_segm_date fsd, flight_perd_segm fps
        WHERE fpl.flight_number = '%s'
        AND fsd.flight_date BETWEEN '%s' AND '%s'
        AND fpl.leg_number >= 0
        AND fp.flgt_sched_status IN ('S','A', 'R', 'D', 'M', 'U')
        AND fp.flight_number = fpl.flight_number
        AND fsd.flight_number = fpl.flight_number
        AND fps.flight_number = fpl.flight_number
        AND fps.schd_perd_no = fpl.schd_perd_no
        AND fsd.schd_perd_no = fpl.schd_perd_no
        AND fp.schd_perd_no = fpl.schd_perd_no
        AND fp.schd_perd_no = fsd.schd_perd_no
        AND fps.schd_perd_no = fsd.schd_perd_no
        AND fp.flgt_sched_status = fsd.flgt_sched_status
        AND fpl.leg_number = fsd.leg_number
        AND fsd.segment_number = fps.segment_number
        AND fp.frequency_code LIKE '____5__'
        ORDER BY fp.start_date, fpl.schd_perd_no, fpl.leg_number
        """ \
            % (flight.flight_number, sdate.strftime("%m/%d/%Y"), edate.strftime("%m/%d/%Y"))
    printlog(2, FbSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FbSql)
    n = 0
    for row in cur:
        print "\t leg %d sched period %d status %s start %s end %s aircraft code %s config table %s frequency %s" \
            % (row['ln'], row['spn'], row['fss'], row['sd'], row['ed'], row['acd'], row['ctn'], row['fc'])
        n += 1

    if n == 0:
        print "\t not found"



def CheckSsmTim(conn, flight, sdate, edate, frequency_code, aircraft_code, schd_perd_no=None):

    ReadAbsoluteRange(conn, flight)

    print "TIM check for flight %s from %s to %s" \
        % (flight.flight_number, sdate.strftime("%Y-%m-%d"), edate.strftime("%Y-%m-%d"))

    CheckFlight(conn, flight.flight_number, flight.departure_time)
    ReadFlightPeriods(conn, flight.flight_number, schd_perd_no)
    ReadFlightPerdLegs(conn, flight.flight_number, schd_perd_no)
    if aircraft_code is not None:
        ReadAircraftConfig(conn, aircraft_code, None, None)

