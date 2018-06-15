# @file ReadSeatReservation.py
"""Read seat reservations."""
import sys
import operator
import psycopg2
from datetime import datetime, timedelta, datetime
from BarsLog import set_verbose, get_verbose, printlog
from Booking.ReadBookingRef import ReadBookNo


def CheckItenary(conn, flight_number, flight_date, depr_airport, book_no):
    """Itenary for booking."""
    print("Itenary for booking %d flight %s on %s"
          % (book_no, flight_number, flight_date))
    RcSql = \
        "SELECT book_no FROM itenary WHERE " \
        " flight_number = '%s' AND   " \
        " flight_date  = '%s' AND " \
        " book_no  = %d    AND " \
        " reserve_status[1,2] not in ('XX', 'XK') " \
        % (flight_number, flight_date.strftime("%m/%d/%Y"), book_no)
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        print("%s" % str(row['book_no'] or ''))
        n += 1
    if n == 0:
        print("No itenary for booking %d flight %s on %s"
              % (book_no, flight_number, flight_date))
    return n


def CheckSeatReservationEtAsr(conn, flight, seat_row_code, bno):
    """First seat reservation check, with booking number."""
    flight_number = flight.flight_number
    flight_date = flight.board_date
    depr_airport = flight.departure_airport

    book_no = int(bno)
    print("Check booking %d seat reservation for flight %s date %s seat %s" \
        % (book_no, flight_number, flight_date.strftime("%Y-%m-%d"),
           seat_row_code))
    n = len(seat_row_code)
    if n > 2:
        seat_row = int(seat_row_code[0:2])
        seat_code = seat_row_code[2]
    else:
        seat_row = int(seat_row_code[0])
        seat_code = seat_row_code[1]
    printlog("Seat row %d code %s" % (seat_row, seat_code))
    RcSql = \
        "SELECT flight_seat_reservation_group_id" \
        " FROM flight_seat_reservation" \
        " WHERE" \
        " flight_date_leg_id IN (" \
        "  SELECT fdl.flight_date_leg_id" \
        "   FROM flight_date_leg AS fdl" \
        "   WHERE fdl.flight_number = '%s'" \
        "   AND fdl.board_date = '%s' )" \
        " AND seat_definition_id IN (" \
        "   SELECT sd.seat_definition_id" \
        "    FROM seat_definition AS sd" \
        "    WHERE sd.row_number = %d AND sd.seat_code = '%s' )" \
        " AND book_no = %d" \
        " AND (blocked_flag IS NULL OR blocked_flag <> 'Y')" \
        " AND temporary_reserve_flag = 'Y'" \
        " AND active_flag = 'A'" \
        % (flight_number, flight_date.strftime("%m/%d/%Y"), seat_row,
           seat_code, book_no)
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    print("\tSeat reservations for booking %d for flight %s on %s seat %s :" \
        % (book_no, flight_number, flight_date.strftime("%Y-%m-%d"),
           seat_row_code), end=' ')
    for row in cur:
        print(" %s" % str(row['flight_seat_reservation_group_id'] or ''), end=' ')
        n += 1

    if n == 0:
        print("not found", end=' ')
    print('')
    return n


# Second seat reservation check, with no booking number
def CheckSeatReservation2(conn, flight_number, flight_date, depr_airport,
                          seat_row_code, book_no=None):

    print("Check seat reservation for flight %s on %s seat %s" \
        % (flight_number, flight_date.strftime("%Y-%m-%d"), seat_row_code))
    n = len(seat_row_code)
    if n > 2:
        seat_row = int(seat_row_code[0:2])
        seat_code = seat_row_code[2]
    else:
        seat_row = int(seat_row_code[0])
        seat_code = seat_row_code[1]
    RcSql = \
        "SELECT flight_seat_reservation_group_id" \
        " FROM flight_seat_reservation" \
        " WHERE flight_date_leg_id IN (" \
        "    SELECT fdl.flight_date_leg_id" \
        "    FROM flight_date_leg AS fdl" \
        "    WHERE fdl.flight_number = '%s' AND fdl.board_date = '%s' )" \
        " AND seat_definition_id IN (" \
        "    SELECT sd.seat_definition_id" \
        "    FROM seat_definition AS sd" \
        "    WHERE sd.row_number = %d AND sd.seat_code = '%s' )" \
        " AND book_no IS NULL" \
        " AND (blocked_flag IS NULL OR blocked_flag <> 'Y')" \
        " AND temporary_reserve_flag = 'Y'" \
        " AND active_flag = 'A'" \
        % (flight_number, flight_date.strftime("%m/%d/%Y"), seat_row, seat_code)
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    print("\tNull reservations for flight leg %s on %s seat %s :" \
        % (flight_number, flight_date, seat_row_code), end=' ')
    for row in cur:
        print(" %s" % str(row['flight_seat_reservation_group_id'] or ''), end=' ')
        n += 1

    if n == 0:
        print(" not found", end=' ')
    print('')
    return n


# API call for seat reservation
def CheckSeatReservation(conn, flight_number, flight_date, depr_airport,
                         seat_row_code, book_no=None):

    if book_no is not None:
        rval = None
        # rval = CheckSeatReservation1(conn, flight_number, flight_date,
        #                              depr_airport, seat_row_code, book_no)
    else:
        rval = CheckSeatReservation2(conn, flight_number, flight_date,
                                     depr_airport, seat_row_code)
    return rval


def ReadSeatReservationId(conn, flight_number, flight_date, status_flag,
                          release_date_time):

    print("Seat reservation ID for flight %s on %s :" \
        % (flight_number, flight_date))
    RcSql = \
        "SELECT flight_seat_reservation_group_id,flight_seat_reservation_id," \
        "flight_date_leg_id, book_no, release_date_time," \
        "seat_definition_id, blocked_flag,temporary_reserve_flag,active_flag" \
        " FROM flight_seat_reservation" \
        " WHERE flight_date_leg_id IN (" \
        "  SELECT fdl.flight_date_leg_id" \
        "  FROM flight_date_leg AS fdl" \
        "  WHERE fdl.flight_number = '%s'" \
        "  AND fdl.board_date = '%s')" \
            % (flight_number, flight_date.strftime("%m/%d/%Y"))
    if status_flag != '*':
        RcSql += \
            " AND (blocked_flag IS NULL OR blocked_flag <> 'Y')" \
            " AND temporary_reserve_flag = 'Y'"
    elif status_flag == 'Y':
        RcSql += \
            " AND (blocked_flag IS NULL OR blocked_flag <> 'Y')" \
            " AND temporary_reserve_flag = 'Y'"
    elif status_flag == 'N':
        RcSql += \
            " AND (blocked_flag IS NULL OR blocked_flag <> 'N')" \
            " AND temporary_reserve_flag = 'N'"
    if release_date_time is not None:
        RcSql += \
            " AND release_date_time >= '%s'" \
                % release_date_time .strftime("%Y-%m-%d %h:%m:%s")
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        sdi = int(row['seat_definition_id'] or 0)
        fsri = int(row['flight_seat_reservation_id'] or 0)
        #print("Seat definition ID %d" % sdi)
        print("\t%8s %8d %8s %8d %20s %8d %3s %3s %3s" \
            % (str(row['flight_seat_reservation_group_id'] or ''), fsri,
               row['flight_date_leg_id'], int(row['book_no']or 0),
               str(row['release_date_time'] or ''), sdi,
               str(row['blocked_flag'] or ''),
               str(row['temporary_reserve_flag'] or ''),
               str(row['active_flag'] or '')))
        if get_verbose() >= 2:
            ReadSeatAttribute(conn, sdi)
            ReadDcsSeat(conn, fsri)
        n += 1

    return n

    if n == 0:
        print("No seat reservation ID for flight %s on %s" \
            % (flight_number, flight_date))
    return n


def ReadSeatReservation(conn, flight_number, flight_date, seat_row_code):

    n = len(seat_row_code)
    if n > 2:
        seat_row = int(seat_row_code[0:2])
        seat_code = seat_row_code[2]
    else:
        seat_row = int(seat_row_code[0])
        seat_code = seat_row_code[1]
    print("Reservations for flight %s date %s seat %d%s :" \
        % (flight_number, flight_date.strftime("%Y-%m-%d"), seat_row, seat_code))
    RcSql = \
        "SELECT flight_seat_reservation_group_id,book_no,release_date_time," \
        "seat_definition_id" \
        " FROM flight_seat_reservation" \
        " WHERE" \
        "  flight_date_leg_id IN (" \
        "          SELECT fdl.flight_date_leg_id" \
        "          FROM flight_date_leg AS fdl" \
        "          WHERE fdl.flight_number = '%s'" \
        "          AND fdl.board_date = '%s' )" \
        " AND seat_definition_id IN (" \
        "          SELECT sd.seat_definition_id" \
        "          FROM seat_definition AS sd" \
        "          WHERE sd.row_number = %d" \
        "          AND sd.seat_code = '%s' )" \
        % (flight_number, flight_date.strftime("%m/%d/%Y"), seat_row,
           seat_code)
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        print("\tbook %8d seat definition %8s seat group %8s" \
            % (row['book_no'], row['seat_definition_id'],
               str(row['flight_seat_reservation_group_id'] or '-')))
        n += 1

    if n == 0:
        print("\tnot found")

    return n


# Read flight date leg
def ReadFlightDateLegInfo(conn, flight_number, flight_date):

    print("Flight date leg for flight %s date %s" % (flight_number, flight_date))
    RcSql = \
        "SELECT trim(flight_number) fn,departure_time,origin_airport_code," \
        "destination_airport_code,leg_number" \
        " FROM flight_date_leg" \
        " WHERE flight_number = '%s' AND board_date = '%s'"  \
        % (flight_number, flight_date.strftime("%m/%d/%Y"))
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    origin_airport = None
    destination_airport = None
    departure_time = None
    for row in cur:
        origin_airport = row['origin_airport_code']
        destination_airport = row['destination_airport_code']
        departure_time = row['departure_time']
        print("\tdepart %s time %s arrive %s" \
            % (origin_airport, departure_time, destination_airport))
        n += 1

    if n == 0:
        print("No flight info for %s on %s" % (flight_number, flight_date))
    return n, origin_airport, destination_airport, departure_time

# Read attributes for seat definition ID
def ReadSeatAttribute(conn, seat_definition_id):

    print("\t\tSeat attributes for seat definition ID %d : " % seat_definition_id, end=' ')
    RcSql = \
        "SELECT seat_attribute_rcd FROM seat_attribute" \
        " WHERE seat_definition_id=%d" % seat_definition_id
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        print("%s" % row['seat_attribute_rcd'], end=' ')
        n += 1
    if n == 0:
        print("not found", end=' ')
    print('')


# Check seat definition
def ReadSeatDefinition(conn, seat_row_code=None, seat_definition_id=None):

    if seat_row_code is not None:
        n = len(seat_row_code)
        if n > 2:
            seat_row = int(seat_row_code[0:2])
            seat_code = seat_row_code[2]
        else:
            seat_row = int(seat_row_code[0])
            seat_code = seat_row_code[1]
        print("Seat definitions for seat code %d%s :" % (seat_row, seat_code))
        RcSql = \
                "SELECT seat_definition_id sdi,seat_map_id," \
                "start_selling_time,stop_selling_time," \
                "block_reserve_reason_rcd" \
                " FROM seat_definition" \
                " WHERE row_number = %d" \
                " AND seat_code = '%s'" \
                % (seat_row, seat_code)
    elif seat_definition_id is not None:
        print("Seat definitions for ID %d :" % seat_definition_id)
        RcSql = \
                "SELECT seat_definition_id sdi,seat_map_id," \
                "start_selling_time,stop_selling_time," \
                "block_reserve_reason_rcd" \
                " FROM seat_definition" \
                " WHERE seat_definition_id=%d" % seat_definition_id
    else:
        print("No seat code or definition ID supplied")
        return -1
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    #print("\t%5s %5s %5s %5s %s" % ("ID", "Map", "Start", "Stop", "Block reserve"))
    for row in cur:
        print("\tseat def %5d map %5d start %5d stop %5d reason %s" \
            % (row['sdi'], row['seat_map_id'], row['start_selling_time'],
               row['stop_selling_time'],
               str(row['block_reserve_reason_rcd'] or '')))
        ReadFlightSeatMap(conn, row['seat_map_id'])
        n += 1
    if n == 0:
        print("\tNo seat definitions for %d%s" % (seat_row, seat_code))
    print('')
    return n


def ReadFlightSeatMap(conn, seat_map_id, recCount=1):

    print("\t\tFlight date legs for seat map ID %d :" % seat_map_id, end=' ')
    RcSql = \
        "SELECT"
    if recCount:
        RcSql += \
            " FIRST %d" % recCount
    RcSql += \
        " flight_date_leg_id FROM flight_seat_map WHERE seat_map_id=%d" \
            % seat_map_id
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        print(" %d" % row['flight_date_leg_id'], end=' ')
        n += 1

    if n == 0:
        print(" not found", end=' ')
    print


def ReadFlightDateLegId(conn, flight_date_leg_id, flight_number, board_date):

    flight_date_leg_ids = []
    print("Flight date leg for %d" % flight_date_leg_id)
    RcSql = \
        "SELECT flight_date_leg_id,trim(flight_number) fn,board_date," \
        "departure_time,origin_airport_code,destination_airport_code," \
        "leg_number" \
        " FROM flight_date_leg WHERE flight_date_leg_id=%d"  \
        % flight_date_leg_id
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        fli = int(row['flight_date_leg_id'] or 0)
        flight_date_leg_ids.append(fli)
        print("%d %s %s %s %s %s %d" \
            % (fli, str(row['fn'] or ''), row['board_date'],
               row['departure_time'], row['origin_airport_code'],
               row['destination_airport_code'], row['leg_number']))
        n += 1

    if n == 0:
        print("No flight date leg for %d" % flight_date_leg_id)
    return n, flight_date_leg_ids


# Also see function ReserveSeats() in asr_service.ecpp
def ReserveSeats(conn, flight_number, board_dts, origin_airport,
                 destination_airport, seat_number,
                 selling_cls_code='Y', str_block_flag='Y'):

    print("Reservations for flight %s on %s from %s to %s seat %s class %s block flag %s" \
        % (flight_number, board_dts.strftime("%Y-%m-%d"), origin_airport,
           destination_airport, seat_number, selling_cls_code, str_block_flag))
    board_date = board_dts.strftime("%m/%d/%Y")
    RcSql = \
        "SELECT sd.seat_definition_id sid, sd.row_number srn, sd.seat_code ssc, fdl.flight_date_leg_id  fid" \
        " FROM flight_date_leg AS fdl " \
        " INNER JOIN flight_seat_map AS fsm ON fsm.flight_date_leg_id = fdl.flight_date_leg_id " \
        " INNER JOIN seat_map AS sm ON sm.seat_map_id = fsm.seat_map_id " \
        " INNER JOIN seat_map_class AS smc ON smc.seat_map_id = sm.seat_map_id AND smc.selling_cls_code = '%s' AND '%s'='N' " \
        " INNER JOIN seat_definition AS sd ON sd.seat_map_id = sm.seat_map_id " \
        "  AND (((fdl.board_date::datetime year to day::varchar(10) || ' ' || fdl.departure_time::varchar(8))::datetime year to minute - CURRENT)::interval hour(4) to hour::varchar(10)::int " \
        "    BETWEEN sd.stop_selling_time AND sd.start_selling_time OR '%s' = 'Y') " \
        " INNER JOIN flight_segm_date as fsd on fsd.flight_number = fdl.flight_number " \
        "  AND fsd.flight_date = fdl.flight_date AND fsd.depr_airport = fdl.origin_airport_code " \
        "  AND fsd.arrv_airport = fdl.destination_airport_code " \
        "  AND fsd.departure_time=(fdl.departure_time-'00:00'::datetime hour to minute)::interval minute(4) to minute::varchar(10)::int " \
        " LEFT JOIN flight_seat_reservation AS fsr ON fsr.flight_date_leg_id = fdl.flight_date_leg_id " \
        "  AND fsr.seat_definition_id = sd.seat_definition_id AND fsr.active_flag = 'A' " \
        "  AND (fsr.release_date_time >= CURRENT OR fsr.temporary_reserve_flag = 'N' OR fsr.temporary_reserve_flag IS Null ) " \
        " WHERE fdl.flight_number = '%s' AND fdl.board_date = '%s' AND fdl.origin_airport_code = '%s' AND fdl.destination_airport_code = '%s' " \
        "  AND fsr.flight_seat_reservation_id IS NULL " \
        "  AND (sd.row_number || sd.seat_code = '%s') " \
        " ORDER BY sd.row_number, sd.seat_code" \
            % (selling_cls_code, str_block_flag, str_block_flag, flight_number, board_date, \
               origin_airport, destination_airport, seat_number)
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        print("\tseat def %s seat %s%s leg id %s" \
            % (row['sid'], row['srn'], row['ssc'], row['fid']))
        n += 1
    return n


def GetFlightDateLegId(conn, flight_number, board_dts, origin_airport,
                       destination_airport):

    print("Flight date leg ID for flight %s on %s" \
        % (flight_number, board_dts.strftime("%Y-%m-%d")))
    board_date = board_dts.strftime("%m/%d/%Y")
    RcSql = \
        "SELECT flight_date_leg_id FROM flight_date_leg" \
        " WHERE flight_number='%s' AND board_date='%s'" \
        " AND origin_airport_code='%s' AND destination_airport_code='%s'" \
            % (flight_number, board_date, origin_airport, destination_airport)
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    flight_date_leg_id = None
    for row in cur:
        flight_date_leg_id = row['flight_date_leg_id']
        print("\t%s" % (flight_date_leg_id))

    if flight_date_leg_id is None:
        print("\tCould not find flight leg ID")

    return flight_date_leg_id


def GetSeatMapId(conn, flight_date_leg_id):

    print("Seat map ID for flight_date_leg_id %d" % flight_date_leg_id)
    seat_map_id = None
    RcSql = \
        "SELECT seat_map_id FROM flight_seat_map" \
        " WHERE flight_date_leg_id=%d" % flight_date_leg_id
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    for row in cur:
        seat_map_id = row['seat_map_id']
        print("\t%d" % seat_map_id)

    if seat_map_id is None:
        print("\tSeat map ID not found")

    return seat_map_id


def GetSeatDefinitionId(conn, seat_map_id, seat_number):

    print("Seat definition ID for seat %s and seat_map_id %d" \
        % (seat_number, seat_map_id))
    seat_definition_id = None
    RcSql = \
        "SELECT seat_definition_id, seat_map_id, default_blocked_flag" \
        " FROM seat_definition" \
        " WHERE seat_map_id=%d AND ((row_number || seat_code) = '%s')" \
            % (seat_map_id, seat_number)
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    for row in cur:
        seat_definition_id = row['seat_definition_id']
        print("\tseat def %s map %s blocked %s" \
            % (seat_definition_id, row['seat_map_id'],
               row['default_blocked_flag']))

    if seat_definition_id is None:
        print("\tSeat definition ID not found")

    return seat_definition_id


def GetFlightSeatReservationId(conn, flight_date_leg_id, seat_definition_id):

    print("Flight seat reservation for flight date leg %d seat definition %d" \
        % (flight_date_leg_id, seat_definition_id))
    flight_seat_reservation_id = None
    RcSql = \
        "SELECT flight_seat_reservation_id,flight_seat_reservation_group_id," \
        "book_no, updt_date_time" \
        " FROM flight_seat_reservation" \
        " WHERE flight_date_leg_id=%d AND seat_definition_id=%d" \
        % (flight_date_leg_id, seat_definition_id)
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    for row in cur:
        flight_seat_reservation_id = row['flight_seat_reservation_id']
        print("\tflight seat reservation ID %8d group ID %8d booking %8d" \
            % (flight_seat_reservation_id,
               row['flight_seat_reservation_group_id'], row['book_no']))

    if flight_seat_reservation_id is None:
        print("\tnot found")

    return flight_seat_reservation_id


def GetSeatMapClass(conn, seat_map_id, selling_cls_code):

    print("Seat map class for seat_map_id %d selling_cls_code %s" \
        % (seat_map_id, selling_cls_code))
    RcSql = \
        "SELECT seat_map_id, selling_cls_code FROM seat_map_class" \
        " WHERE seat_map_id=%d AND selling_cls_code='%s'" \
            % (seat_map_id, selling_cls_code)
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    m = 0
    for row in cur:
        print("\t%d %s" % (row['seat_map_id'], row['selling_cls_code']))
        m += 1

    if m == 0:
        print("Seat map class not found")

    return m


# Also see ReserveSeats() in asr_service.ecpp
def ReadReserveSeats(conn, flight_number, board_dts,
                     origin_airport, destination_airport, seat_numbers,
                     selling_cls_code='Y', str_block_flag='Y'):

    flight_date_leg_id = GetFlightDateLegId(conn, flight_number, board_dts,
                                            origin_airport,
                                            destination_airport)
    if flight_date_leg_id is None:
        return 1

    seat_map_id = GetSeatMapId(conn, flight_date_leg_id)
    if seat_map_id is None:
        return 1

    m = GetSeatMapClass(conn, seat_map_id, selling_cls_code)
    if m == 0:
        return 1

    for seat_number in seat_numbers:
        print("___________________________________")
        print("Check reserved seat %s with seat_map_id %d" % (seat_number, seat_map_id))
        seat_definition_id = GetSeatDefinitionId(conn, seat_map_id, seat_number)
        if seat_definition_id is None:
            return 1

        flight_seat_reservation_id = GetFlightSeatReservationId(conn,
                                                                flight_date_leg_id,
                                                                seat_definition_id)
        if flight_seat_reservation_id is None:
            return 1

    return 0


def FlightSeatBookings(conn, flight_number, flight_date,
                       origin_airport, destination_airport):

    flight_date_leg_id = GetFlightDateLegId(conn, flight_number, flight_date,
                                            origin_airport, destination_airport)
    if flight_date_leg_id is None:
        return 1

    seat_map_id = GetSeatMapId(conn, flight_date_leg_id)
    if seat_map_id is None:
        return 1

    print("Flight seat reservations for flight date leg id %d" \
        % (flight_date_leg_id))
    flight_seat_reservation_id = None
    RcSql = \
        "SELECT flight_seat_reservation_id,flight_seat_reservation_group_id," \
        "fsr.seat_definition_id sdi,book_no,fsr.updt_date_time," \
        "row_number||seat_code seat" \
        " FROM flight_seat_reservation fsr, seat_definition sd" \
        " WHERE flight_date_leg_id=%d" \
        " AND fsr.seat_definition_id=sd.seat_definition_id" \
        " ORDER BY fsr.seat_definition_id" \
            % flight_date_leg_id
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    for row in cur:
        flight_seat_reservation_id = int(row['flight_seat_reservation_id'])
        if get_verbose() >= 1:
            print("\tseat reserve id %8d group reserve id %8d book %8d seat def id %8d" \
                % (flight_seat_reservation_id,
                   int(row['flight_seat_reservation_group_id']),
                   int(row['book_no'] or 0), row['sdi']), end=' ')
            print(" : %4s" % row['seat'])
        else:
            print("\tbook %8d seat id %8d" \
                % (int(row['book_no'] or 0), row['sdi']), end=' ')
            print(" : %4s" % row['seat'])

    if flight_seat_reservation_id is None:
        print("Flight seat reservation ID not found")

    return 0


def ReadDcsSeat(conn, flight_seat_reservation_id):

    print("\t\tDCS seat info for flight_seat_reservation_id %d : " \
        % flight_seat_reservation_id, end=' ')
    RcSql = \
        "SELECT seat_number,dcs_passenger_id,dcs_itinerary_id," \
        "boarding_control_number" \
        " FROM dcs_seat WHERE flight_seat_reservation_id=%d" \
            % flight_seat_reservation_id
    printlog(RcSql, 2)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        print("%s %s %s %s %s" \
            % (row['seat_number'], row['dcs_passenger_id'],
               row['dcs_itinerary_id'], row['boarding_control_number']), end=' ')
        n += 1
    if n == 0:
        print("not found", end=' ')
    print('')
    return n
