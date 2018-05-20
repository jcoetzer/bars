# @file ReadFlights.py

import sys
import psycopg2
import psycopg2.extras
from BarsLog import set_verbose, get_verbose, printlog
from ReadDateTime import ReadDate
from FlightData import FlightData


def GetFlightDataSsm(conn, flight_number, fd1, fd2, freq=None):

    if freq is None:
        board_weekday = int(fd1.board_dts.strftime("%w"))
        # Convert to 1(Monday) to 7(Sunday)
        if board_weekday == 0:
            board_weekday = 7
        freq = "%%%d%%" % board_weekday
    else:
        freq = freq.replace("-", "_")
    print("SSM data for flight %s board %s to %s frequency '%s'"
          % (flight_number,
             fd1.strftime("%Y-%m-%d"), fd2.strftime("%Y-%m-%d"),
             freq))
    RcSql = \
        "SELECT fpl.schd_perd_no spn,fpl.depr_airport depr, fpl.arrv_airport arrv," \
        "fp.start_date sd,fp.end_date ed,fpl.leg_number ln,fp.via_cities vc," \
        "fp.flgt_sched_status fss,fp.frequency_code fc,fpl.departure_time dt," \
        "fpl.arrival_time,fps.aircraft_code,fpl.config_table_no," \
        "fpl.depr_terminal_no dtn, fpl.arrv_terminal_no atn" \
        " FROM flight_perd_legs fpl,flight_periods fp,flight_segm_date fsd," \
        "flight_perd_segm fps" \
        " WHERE fpl.flight_number = '%s'" \
        " AND fsd.flight_date BETWEEN '%s' AND '%s'" \
        " AND fpl.leg_number>=0" \
        " AND fp.flgt_sched_status IN ('S','A', 'R', 'D', 'M', 'U')" \
        " AND fp.flight_number=fpl.flight_number" \
        " AND fsd.flight_number=fpl.flight_number" \
        " AND fps.flight_number=fpl.flight_number" \
        " AND fps.schd_perd_no=fpl.schd_perd_no" \
        " AND fsd.schd_perd_no=fpl.schd_perd_no" \
        " AND fp.schd_perd_no=fpl.schd_perd_no" \
        " AND fp.schd_perd_no=fsd.schd_perd_no" \
        " AND fps.schd_perd_no=fsd.schd_perd_no" \
        " AND fp.flgt_sched_status=fsd.flgt_sched_status" \
        " AND fpl.leg_number=fsd.leg_number" \
        " AND fsd.segment_number=fps.segment_number" \
        " AND fp.frequency_code LIKE '%s'" \
        " ORDER BY fp.start_date, fpl.schd_perd_no, fpl.leg_number" \
        % (flight_number, fd1.strftime("%m/%d/%Y"), fd2.strftime("%m/%d/%Y"), freq)
    printlog(2, RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        print("\t sched perd %s depart %s arrive %s from %s to %s via %s"
              % (row['spn'], row['depr'], row['arrv'], row['sd'],
                 row['ed'], row['vc']))
        n += 1

    if n == 0:
        print "\tnot found"


def ReadFlightInformation(conn, flight_number, flight_date):

    print "Flight information for flight %s board %s [flight_information]" \
        % (flight_number, flight_date.strftime("%Y-%m-%d"))
    RcSql = \
        "SELECT depr_airport,arrv_airport,remarks,user_name" \
        " FROM flight_information" \
        " WHERE flight_number = '%s'" \
        " AND board_date = '%s'" \
            % (flight_number, flight_date.strftime("%m/%d/%Y"))
    printlog(2, RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        print "\tdepart %s arrive %s remark '%s'" \
            % (row['depr_airport'], row['arrv_airport'], row['remarks'])
        n += 1

    if n == 0:
        print "\tnot found"

    return


def ReadCodeShare(conn, flight_number, board_date_mdy):

    printlog(1, "Codeshares for flight %6s on %s:" % (flight_number, board_date_mdy))
    RcSql = \
        "SELECT flight_number, dup_flight_number" \
        " FROM flight_shared_leg fsl" \
        " WHERE (fsl.flight_number = '%s' OR fsl.dup_flight_number = '%s')" \
        " AND fsl.board_date = '%s'" \
            % (flight_number, flight_number, board_date_mdy)
    printlog(2, RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    cs = None
    for row in cur:
        if flight_number != row['flight_number'] :
            #print " %6s" % row['flight_number'],
            cs = row['flight_number']
        if flight_number != row['dup_flight_number'] :
            cs = row['dup_flight_number'],
    printlog(1, "Codeshare %s" % cs)
    return cs


def SetCodeShare(conn, flight):

    # flight.display(False)
    #print "Codeshares for flight %6s board %s:" % (flight.flight_number, flight.board_date_iso),
    # print " codeshare : ",
    RcSql = \
        "SELECT flight_number, dup_flight_number" \
        " FROM flight_shared_leg fsl" \
        " WHERE (fsl.flight_number = '%s' OR fsl.dup_flight_number = '%s')" \
        " AND fsl.board_date = '%s'            " \
            % (flight.flight_number, flight.flight_number, flight.board_date_mdy)
    printlog(2, RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    codeshares = []
    for row in cur:
        if flight.flight_number != row['flight_number']:
            flight.update_codeshare(row['flight_number'])
            codeshares.append(row['flight_number'])
        if flight.flight_number != row['dup_flight_number']:
            flight.update_codeshare(row['dup_flight_number'])
            codeshares.append(row['dup_flight_number'])
    #print
    return codeshares


def ReadFlightDateClassSeatMaps(conn, flight):

    flight_number    = flight.flight_number
    flight_date      = flight.board_dts
    classCode        = flight.class_code
    departureAirport = flight.departure_airport
    arrivalAirport   = flight.arrival_airport

    RcSql = \
        "SELECT sm.seat_map_id smid, sm.description desc, sm.image_url_path url, sm.image_width iw, sm.image_height ih," \
        "  sm.block_image bimg, sm.reserve_image rimg, sm.vacant_image vimg, sm.unavailable_image uimg, " \
        "  sm.seat_width smw, sm.seat_height smh" \
        " FROM flight_date_leg AS fdl " \
        "  INNER JOIN flight_seat_map AS fsm ON fsm.flight_date_leg_id = fdl.flight_date_leg_id" \
        "  INNER JOIN seat_map AS sm ON sm.seat_map_id = fsm.seat_map_id" \
        "  INNER JOIN seat_map_class AS smc ON smc.seat_map_id = sm.seat_map_id" \
        " WHERE fdl.flight_number = '%s'" \
        "  AND fdl.board_date = '%s'" \
        "  AND fdl.origin_airport_code = '%s'" \
        "  AND fdl.destination_airport_code = '%s'" \
        "  AND smc.selling_cls_code = '%s'" \
        % (flight_number, flight_date.strftime("%m/%d/%Y"), departureAirport, arrivalAirport, classCode)
    printlog(RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    print "Flight %6s on %10s from %3s to %3s : " % (flight_number, flight_date.strftime("%Y-%m-%d"), departureAirport, arrivalAirport),
    n = 0
    for row in cur:
        n += 1
        if n > 1: print "\n       %6s    %10s      %3s    %3s   " % ('', '', '', ''),
        print "seat map %s (%s)" % (row['smid'], row['desc']),
    if n == 0: print "seat map not found",
    print


def CheckFlightDateClassSeatMaps(conn, flight):

    flight_number    = flight.flight_number
    flight_date      = flight.board_dts
    classCode        = flight.class_code
    departureAirport = flight.departure_airport
    arrivalAirport   = flight.arrival_airport

    print "Flight %6s on %10s from %3s to %3s : " \
        % (flight_number, flight_date.strftime("%Y-%m-%d"), departureAirport,
           arrivalAirport)
    RcSql = \
        "SELECT flight_date_leg_id FROM flight_date_leg" \
        " WHERE flight_number = '%s'" \
        "  AND board_date = '%s'" \
            % (flight_number, flight_date.strftime("%m/%d/%Y"))
    printlog(RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        flight_date_leg_id = int(row['flight_date_leg_id'])
        print "Flight leg ID %d" % flight_date_leg_id

        # Read flight_seat_map
        RcSql2 = \
            "SELECT sm.seat_map_id smi" \
            " FROM flight_seat_map sm WHERE flight_date_leg_id=%d" \
                % (flight_date_leg_id)
        printlog(RcSql2)
        cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur2.execute(RcSql2)
        n = 0
        for row2 in cur2:
            seat_map_id = int(row2['smi'])
            print "\t Seat map ID %d" % (seat_map_id)
            #"SELECT sm.seat_map_id smid, sm.description desc, sm.image_url_path url, sm.image_width iw, sm.image_height ih," \
            #"  sm.block_image bimg, sm.reserve_image rimg, sm.vacant_image vimg, sm.unavailable_image uimg, " \
            #"  sm.seat_width smw, sm.seat_height smh" \
            #" FROM flight_date_leg AS fdl " \
            #"  INNER JOIN flight_seat_map AS fsm ON fsm.flight_date_leg_id = fdl.flight_date_leg_id" \
            #"  INNER JOIN seat_map AS sm ON sm.seat_map_id = fsm.seat_map_id" \
            #"  INNER JOIN seat_map_class AS smc ON smc.seat_map_id = sm.seat_map_id" \
            #" WHERE fdl.flight_number = '%s'" \
            #"  AND fdl.board_date = '%s'" \
            #"  AND fdl.origin_airport_code = '%s'" \
            #"  AND fdl.destination_airport_code = '%s'" \
            #"  AND smc.selling_cls_code = '%s'" \
            #% (flight_number, flight_date.strftime("%m/%d/%Y"), departureAirport, arrivalAirport, classCode)

        # Read seat_map
        RcSql2 = \
            "SELECT description" \
            " FROM seat_map sm WHERE seat_map_id=%d" \
                % (seat_map_id)
        printlog(RcSql2)
        cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur2.execute(RcSql2)
        for row2 in cur2:
            print "\t Description '%s'" % row2['description']

        # Read seat_map_class
        RcSql2 = \
            "SELECT selling_cls_code" \
            " FROM seat_map_class sm WHERE seat_map_id=%d" \
                % (seat_map_id)
        printlog(RcSql2)
        cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur2.execute(RcSql2)
        for row2 in cur2:
            print "\t Class '%s'" % row2['selling_cls_code']
        n += 1

    if n == 0:
        print "Seat map not found"
    print


def ReadDeparture(conn, flight_number, flight_date, delim=' '):

    RcSql = \
            "select depr_airport,arrv_airport, city_pair_no from flight_segm_date" \
            " where flight_number='%s' and flight_date='%s'" % (flight_number, flight_date.strftime("%m/%d/%Y"))
    printlog(2, RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    rval = ""
    rval2 = ""
    rval3 = 0
    for row in cur:
        if n:
            rval += delim
            rval2 += delim
            #rval3 += delim
        rval += str(row['depr_airport'] or '')
        rval2 += str(row['arrv_airport'] or '')
        rval3 += int(row['city_pair_no'] or 0)
        n += 1
        printlog(1, "\tDepart %s arrive %s city pair %d" % (rval, rval2, rval3))

    return n, rval, rval2, rval3


def ReadFlightDeparture(conn, class_code, flight_number, flight_date):

    printlog(1, "Read data for flight %s date %s [flight_segm_date]" % (flight_number, flight_date.strftime("%Y-%m-%d")))
    RcSql = \
            "SELECT depr_airport,arrv_airport, city_pair_no,departure_time,arrival_time,flgt_sched_status,schd_perd_no" \
            " FROM flight_segm_date" \
            " WHERE flight_number='%s' AND flight_date='%s'" \
                % (flight_number, flight_date.strftime("%m/%d/%Y"))
    printlog(RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    flight = None
    for row in cur:
        departure_airport = str(row['depr_airport'] or '')
        arrival_airport   = str(row['arrv_airport'] or '')
        city_pair_no = int(row['city_pair_no'] or 0)
        departure_time = int(row['departure_time'] or 0)
        arrival_time = int(row['arrival_time'] or 0)
        n += 1
        printlog(1, "Flight %s date %s depart %s %d arrive %s %d status %s" % (flight_number, flight_date.strftime("%Y-%m-%d"), \
                 departure_airport, departure_time, arrival_airport, arrival_time, str(row['flgt_sched_status'] or '?')))
        flight = FlightData(class_code, flight_number, flight_date, departure_time, arrival_time, \
                            departure_airport, arrival_airport, city_pair_no,
                            schd_perd_no=int(row['schd_perd_no'] or 0))

    return n, flight


def ReadDepartArrive(conn, flight_number, flight_date, delim=' '):

    RcSql = \
            "SELECT depr_airport,arrv_airport" \
            " FROM flight_segm_date" \
            " WHERE flight_number='%s' AND flight_date='%s'" \
                % (flight_number, flight_date.strftime("%m/%d/%Y"))
    printlog(RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    rval = ""
    for row in cur:
        if n:
            rval += delim
        rval += str(row['depr_airport'] or '')
        rval += '-'
        rval += str(row['arrv_airport'] or '')
        n += 1

    return rval


def GetFlights(conn, dt1, depr_airport, arrv_airport):

    flights = []

    RcSql = \
        "SELECT flight_number FROM flight_segm_date WHERE flight_date='%s' " % \
        dt1.strftime("%m/%d/%Y")
    if depr_airport is not None:
        RcSql += " and depr_airport='%s'" % depr_airport
    if arrv_airport is not None:
        RcSql += " and arrv_airport='%s'" % arrv_airport
    RcSql += " and flight_number like 'JE___'"
    printlog(RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        flights.append(row['flight_number'])
        n += 1

    return flights


def GetLegPostion(strSegmentNumber):

    i = 0
    j = len(strSegmentNumber)
    while i < j:
        if strSegmentNumber[i] == '1':
            break
        i += 1

    return i


def checkForRecentUpdate(conn, flight_number, flight_date, departureAirport, arrivalAirport, classCode):

    IsegSql = \
        "SELECT COUNT(*) FROM inventry_segment" \
        " WHERE flight_number = '%s' AND flight_date = '%s' AND departure_city = '%s' AND arrival_city = '%s' AND selling_cls_code = '%s'" \
        " AND update_time BETWEEN to_char(CURRENT - :timeWindowInSeconds units second, '%Y/%m/%d/%H/%M/%S') AND " \
        "        to_char(CURRENT, '%Y/%m/%d/%H/%M/%S')"


def get_special_service_request_inventory(conn, flight_number, flight_date, city_pair_no):

    print "SSR inventory for flight %s date %s city pair %s [special_service_request_inventory]" \
        % (flight_number, flight_date, city_pair_no)
    IsegSql = \
        "SELECT booking_no, rqst_code" \
        " FROM special_service_request_inventory" \
        " WHERE flight_number='%s' AND flight_date='%s' AND city_pair_no='%s' AND inactivated_date_time IS NULL" \
        % (flight_number, flight_date, city_pair_no)
    printlog(IsegSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(IsegSql)
    n = 0
    for row in cur:
        n += 1
        print "\t book %s request %s" % (row['booking_no'], row['rqst_code'])
    if n == 0:
        print "\tnot found"


"""
Adjust all nett_sold numbers caused by over-arching segments
"""
def nett_sold_reconcile(conn, flight_number, flight_date, class_code):

    IsegSql = \
        "SELECT SUM(segm_sngl_sold),SUM(segm_grup_sold),SUM(segm_nrev_sold)" \
        " FROM inventry_segment" \
        " WHERE flight_number='%s' AND flight_date='%' AND selling_cls_code='%s'" \
        " AND SUBSTR(segment_number, ? ,1) = '1'"
    return


"""
Find all legs and segments for the selling class
"""
def get_inventry_segment_class(conn, flight_number, flight_date, class_code):

    print "Inventory segment class %s for flight %s date %s [inventry_segment]" % (class_code, flight_number, flight_date)
    IsegSql = \
        "SELECT segment_number, segm_sngl_sold, segm_grup_sold, segm_nrev_sold" \
        " FROM inventry_segment" \
        " WHERE flight_number='%s' AND flight_date='%s' AND selling_cls_code='%s'" \
        % (flight_number, flight_date, class_code)
    printlog(IsegSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(IsegSql)
    n = 0
    for row in cur:
        n += 1
        print "\tsegment %s sngl %s grup %s nrev %s" \
            % (row['segment_number'], row['segm_sngl_sold'], row['segm_grup_sold'], row['segm_nrev_sold'])
    if n == 0:
        print "\tnot found"


"""
Find all the legs and segments for the flight
"""
def get_inventry_segment(conn, flight_number, flight_date, reconcile_window):

    print "Inventory segment for flight %s date %s [inventry_segment]" % (flight_number, flight_date)

    IsegSql = \
        "SELECT selling_cls_code, leg_number, segment_number, departure_city, arrival_city" \
        " FROM inventry_segment" \
        " WHERE flight_number = '%s' AND flight_date = '%s'" \
        " ORDER BY selling_cls_code, leg_number" \
        % (flight_number, flight_date)
    printlog(IsegSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(IsegSql)
    n = 0
    for row in cur:
        n += 1
        print "\tclass %s leg %s segment %s depart %s arrive %s" \
            % (row['selling_cls_code'], row['leg_number'], row['segment_number'], row['departure_city'], row['arrival_city'])
        get_inventry_segment_class(conn, flight_number, flight_date, row['selling_cls_code'])
    if n == 0:
        print "\tnot found"


def nett_sold_reconcile(conn):
    return


def ReadFlights(conn, flight_number, dt1, dt2, depr_airport, arrv_airport, code_share=False, class_code='Y', company_code='JE'):

    FsegSql=\
        "SELECT flight_number,flight_date,depr_airport,arrv_airport," \
        "city_pair_no,departure_time,arrival_time,aircraft_code,schd_perd_no" \
        " FROM flight_segm_date WHERE 1=1"
    if flight_number is not None:
        printlog(1, "Flight number %s" % flight_number)
        FsegSql += \
            " AND flight_number='%s'" \
                % (flight_number)
    if dt1 is not None and dt2 is not None:
        printlog(1, "Read flights from date %s to %s [flight_segm_date]" % \
            (dt1.strftime("%Y-%m-%d"), dt2.strftime("%Y-%m-%d")))
        FsegSql += \
            " AND flight_date BETWEEN '%s' AND '%s'" \
                % (dt1.strftime("%m/%d/%Y"), dt2.strftime("%m/%d/%Y"))
    elif dt1 is not None:
        printlog(1, "Read flights for date %s [flight_segm_date]" % dt1.strftime("%Y-%m-%d"))
        FsegSql += \
            " AND flight_date = '%s'" % dt1.strftime("%m/%d/%Y")
    if depr_airport is not None and arrv_airport is not None:
        FsegSql += \
            " AND depr_airport='%s' AND arrv_airport='%s'" \
                % (depr_airport, arrv_airport)
    FsegSql += \
        " ORDER BY flight_date"

    if code_share:
        printlog(1, "With codeshare")

    printlog(2, FsegSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FsegSql)
    flights = []
    for row in cur:
        printlog(1, "Flight %-6s date %s depart %s arrive %s city pair %3d" \
            % (row['flight_number'], row['flight_date'], row['depr_airport'], row['arrv_airport'], int(row['city_pair_no'])))
        flight_number = row['flight_number']
        departure_date = row['flight_date']
        departure_time = int(row['departure_time'])
        arrival_time = int(row['arrival_time'])
        if code_share:
            cs = ReadCodeShare(conn, flight_number, departure_date.strftime('%m/%d/%Y'))
        else:
            cs = None
        flights.append(FlightData(class_code, flight_number, departure_date, departure_time, arrival_time, \
                 row['depr_airport'], row['arrv_airport'], int(row['city_pair_no']), aircraft_code=row['aircraft_code'],
                 schd_perd_no=row['schd_perd_no'], codeshare=cs))

    #printlog(1, "Found %d flights for date %s" % (len(flights), dt1.strftime("%Y-%m-%d")))
    return flights


def ReadFlight(conn, flight_number, dts, class_code='Y'):

    printlog(1, "Read flight %s for date %s [flight_segm_date]" % (flight_number, dts.strftime("%Y-%m-%d")))
    fdate=dts.strftime("%m/%d/%Y")
    FsegSql=\
        "SELECT flight_number,flight_date,depr_airport,arrv_airport," \
        "city_pair_no, departure_time, arrival_time, aircraft_code," \
        "schd_perd_no" \
        " FROM flight_segm_date" \
        " WHERE flight_number = '%s'" \
        " AND flight_date = '%s'" \
        % (flight_number, fdate)
    FsegSql += \
        " ORDER BY flight_date, departure_time"
    printlog(2, FsegSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FsegSql)
    flights = []
    for row in cur:
        flight_number = row['flight_number']
        departure_date = row['flight_date']
        departure_time = row['departure_time']
        arrival_time = row['arrival_time']

        printlog(1, "Flight %-6s date %s depart %s arrive %s city pair %3d" \
            % (flight_number, row['flight_date'], row['depr_airport'], row['arrv_airport'], int(row['city_pair_no'])))
        flights.append(FlightData(class_code, flight_number, departure_date,
                                  departure_time, arrival_time,
                                  row['depr_airport'], row['arrv_airport'],
                                  int(row['city_pair_no']),
                                  aircraft_code=row['aircraft_code'],
                                  schd_perd_no=row['schd_perd_no']))

    printlog(1, "Found %d flights for date %s" % (len(flights), dts.strftime("%Y-%m-%d")), 1)
    if len(flights):
        return flights[0]
    else:
        return None


def CheckFlight(conn, flight_number, dts, class_code='Y'):

    print "Flight segment dates for flight %s date %s [flight_segm_date]" % (flight_number, dts.strftime("%Y-%m-%d"))
    fdate=dts.strftime("%m/%d/%Y")
    FsegSql=\
        "SELECT flight_number,flight_date,depr_airport,arrv_airport," \
        "city_pair_no, departure_time, arrival_time, aircraft_code," \
        "schd_perd_no,flgt_sched_status" \
        " FROM flight_segm_date" \
        " WHERE flight_number = '%s'" \
        " AND flight_date = '%s'" \
        % (flight_number, fdate)
    FsegSql += \
        " ORDER BY flight_date, departure_time"
    printlog(2, FsegSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FsegSql)
    n = 0
    for row in cur:
        print "\tdepart %s %s arrive %s %s city pair %3d schedule period %d aircraft %s status %s" \
            % (row['depr_airport'], str(row['departure_time']),
               row['arrv_airport'], str(row['arrival_time']),
               int(row['city_pair_no']), int(row['schd_perd_no']),
               row['aircraft_code'], str(row['flgt_sched_status'] or '?'))
        n += 1

    printlog(1, "Found %d flights for date %s" % (n, dts.strftime("%Y-%m-%d")))
    return n


def ReadFlightsDate(conn, dts, ndays, depr_airport, arrv_airport, code_share=False, class_code='Y', company_code='JE'):

    printlog(1, "Flights for date %s [flight_segm_date]" % dts.strftime("%Y-%m-%d"))
    if code_share: printlog(1, "With codeshare")
    fdate=dts.strftime("%m/%d/%Y")
    FsegSql=\
        "SELECT DISTINCT flight_number, flight_date, depr_airport, arrv_airport, city_pair_no, departure_time, arrival_time, " \
        "aircraft_code, schd_perd_no" \
        " FROM flight_segm_date" \
        " WHERE (substring(flight_number from 1 for 2) = '%s' OR substring(flight_number from 1 for 3) = '%s')" \
        " AND ( (flight_date = '%s' AND %d = 0) OR (flight_date >= DATE('%s') AND flight_date < (DATE('%s') + %d) AND %d > 0 ))" \
        % (company_code, company_code, fdate, ndays, fdate, fdate, ndays, ndays)
    if depr_airport is not None and arrv_airport is not None:
        FsegSql += \
            " AND depr_airport='%s' AND arrv_airport='%s'" % (depr_airport, arrv_airport)
    FsegSql += \
        " ORDER BY flight_date, departure_time"
    printlog(2, FsegSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FsegSql)
    flights = []
    for row in cur:
        printlog(1, "Flight %-6s date %s depart %s arrive %s city pair %3d" \
            % (row['flight_number'], row['flight_date'], row['depr_airport'], row['arrv_airport'], int(row['city_pair_no'])))
        flight_number = row['flight_number']
        departure_date = row['flight_date']
        departure_time = str(row['departure_time'])
        #arrival_date = ReadDate(row['arrival_date'])
        arrival_time = str(row['arrival_time'])
        if code_share:
            cs = ReadCodeShare(conn, flight_number, fdate)
        else:
            cs = None
        flights.append(FlightData(class_code, flight_number, departure_date, departure_time, arrival_time, \
                       row['depr_airport'], row['arrv_airport'], int(row['city_pair_no']), aircraft_code=row['aircraft_code'],
                       schd_perd_no=row['schd_perd_no'], codeshare=cs))

    printlog(1, "Found %d flights for date %s" % (len(flights), dts.strftime("%Y-%m-%d")))
    return flights


def ReadFlightsDateLeg(conn, dts, ndays, depr_airport, arrv_airport, class_code='Y', company_code='JE'):

    printlog(1, "Flights for date %s [flight_segm_date]" % dts.strftime("%Y-%m-%d"), 1)
    fdate=dts.strftime("%m/%d/%Y")
    FsegSql = \
        "SELECT trim(flight_number) fn, flight_date, board_date, departure_time, origin_airport_code, destination_airport_code, leg_number, schd_perd_no" \
        " FROM flight_date_leg" \
        " WHERE (flight_number[1,2] = '%s' OR flight_number[1,3] = '%s')" \
        " AND board_date = '%s'" \
            % (company_code, company_code, fdate)
    if depr_airport is not None and arrv_airport is not None:
        FsegSql += \
            " AND origin_airport_code='%s' AND destination_airport_code='%s'" % (depr_airport, arrv_airport)
    FsegSql += \
        " ORDER BY fn, flight_date"
    printlog(2, FsegSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FsegSql)
    flights = []
    city_pair_no = 0
    arrv_airport=''
    aircraft_code = ''
    arrival_time = None
    for row in cur:
        flight_number = row['fn']
        departure_date = row['flight_date']
        departure_time = row['departure_time']
        printlog(1, "Flight %-6s date %s depart %s arrive %s" \
            % (flight_number, departure_date, row['origin_airport_code'], row['destination_airport_code']))
        flights.append(FlightData(class_code, flight_number, departure_date, departure_time, arrival_time, \
                       row['origin_airport_code'], row['destination_airport_code'], city_pair_no, aircraft_code,
                       schd_perd_no=row['schd_perd_no']))

    printlog(1, "Found %d flights for date %s" % (len(flights), dts.strftime("%Y-%m-%d")))
    return flights


def ReadFlightSegmDates(conn, dts, ndays, reconcile_window, company_code='JE'):

    fdate=dts.strftime("%m/%d/%Y")
    print "Flight segment dates %s days %d reconcile %s [flight_segm_date]" % (fdate, ndays, reconcile_window)
    FsegSql=\
        "SELECT DISTINCT flight_number, flight_date, depr_airport, arrv_airport, city_pair_no" \
        " FROM flight_segm_date" \
        " WHERE (flight_number[1,2] = '%s' OR flight_number[1,3] = '%s')" \
        " AND ( (flight_date = '%s' AND %d = 0) OR (flight_date >= DATE('%s') AND flight_date < (DATE('%s') + %d) AND %d > 0 ))" \
        " ORDER BY 1, 2" \
        % (company_code, company_code, fdate, ndays, fdate, fdate, ndays, ndays)
    printlog(2, FsegSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FsegSql)
    n = 0
    for row in cur:
        n += 1
        flight_number = row['flight_number']
        print "%-6s %s %s %s %3d" % (row['flight_number'], row['flight_date'], row['depr_airport'], row['arrv_airport'], int(row['city_pair_no']))
        fdate = row['flight_date'].strftime("%m/%d/%Y")
        get_inventry_segment(conn, row['flight_number'], fdate, reconcile_window)
        get_special_service_request_inventory(conn, flight_number, fdate, row['city_pair_no'])
    if n == 0:
        print "\tnot found"

    return n


def ReadFlightSegmDate(conn, flight_number, dts, ndays, reconcile_window):
    CompanyCode='JE'
    fdate=dts.strftime("%m/%d/%Y")
    print "Flight segment dates %s days %d reconcile %s [flight_segm_date]" % (fdate, ndays, reconcile_window)
    FsegSql=\
        "SELECT flight_number, flight_date, depr_airport, arrv_airport, city_pair_no, flgt_sched_status" \
        " FROM flight_segm_date" \
        " WHERE (flight_number = '%s')" \
        " AND ( (flight_date = '%s' AND %d = 0) OR (flight_date >= DATE('%s') AND flight_date < (DATE('%s') + %d) AND %d > 0 ))" \
        " ORDER BY 1, 2" \
        % (flight_number, fdate, ndays, fdate, fdate, ndays, ndays)
    printlog(2, FsegSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FsegSql)
    n = 0
    for row in cur:
        n += 1
        print "\tflight %-6s date %s depart %s arrive %s city pair %3d status %s" \
            % (row['flight_number'], row['flight_date'], row['depr_airport'], row['arrv_airport'], int(row['city_pair_no']),
               row['flgt_sched_status'])
        fdate = row['flight_date'].strftime("%m/%d/%Y")
        get_inventry_segment(conn, row['flight_number'], fdate, reconcile_window)
        get_special_service_request_inventory(conn, flight_number, fdate, row['city_pair_no'])
    if n == 0:
        print "\tnot found"

    return n


# TODO this looks broken
def ReadFLightSeatMap(conn, flight):
    seat_map_id = flight.seat_map_id
    print "Aircraft for seat map ID %d [seat_map]" % seat_map_id
    FdSql = "select aircraft_code from seat_map where seat_map_id='%d'" \
        % (seat_map_id)
    printlog(FdSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FdSql)
    n = 0
    for row in cur:
        n += 1
        aircraft_code = row['aircraft_code']
        print "\taircraft %s" % aircraft_code
    if n == 0:
        print "\tnot found"

    return n, aircraft_desc
