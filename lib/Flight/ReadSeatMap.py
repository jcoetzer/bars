# @file ReadSeatMap.py

import sys
import psycopg2
from BarsLog import set_verbose, get_verbose, printlog
from ReadDateTime import ReadDate
from ReadFlightDateLegs import ReadFlightDateLegId
from ReadFlights import ReadFlight


def ReadSeatMapConfiguration(conn, seat_map_id=None, config_table=None):
    """Read seat map configuration from database."""
    print "Seat map configuration for",
    SmcSql = \
        "SELECT seat_map_id, config_table,update_user,update_time FROM seat_map_configuration"

    if seat_map_id is not None and config_table is not None:
        print "seat map ID %d config table %s" \
            % (seat_map_id, config_table),
        SmcSql += \
            " WHERE seat_map_id=%d AND config_table='%s'" \
                (seat_map_id, config_table)
    elif seat_map_id is not None:
        print "seat map ID %d" % seat_map_id,
        SmcSql += \
            " WHERE seat_map_id=%d" % seat_map_id
    elif config_table is not None:
        print "config table %s" % str(config_table),
        SmcSql += \
            " WHERE config_table='%s'" % str(config_table)
    else:
        print "unspecified seat map and configuration table"
        return
    print "[seat_map_configuration]"

    printlog(SmcSql,2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SmcSql)
    seat_map_id = 0
    n = 0
    config_table = None
    for row in cur:
        n += 1
        config_table = str(row['config_table'] or '???')
        print "\tseat map ID %d config table %s user %s update %s" \
            % (row['seat_map_id'], config_table, row['update_user'], row['update_time'])
    if n==0:
        print "\t not found"

    return config_table


# Read flight seat map from database
def ReadFlightSeatMap(conn, flight_date_leg_id):

    print "Flight seat map for flight date leg ID %d [flight_seat_map]" % flight_date_leg_id
    SmcSql = \
        "SELECT seat_map_id,update_user,update_time" \
        " FROM flight_seat_map WHERE flight_date_leg_id=%d" \
            % flight_date_leg_id
    printlog(SmcSql,2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SmcSql)
    seat_map_id = 0
    n = 0
    for row in cur:
        n += 1
        seat_map_id = int(row['seat_map_id'])
        print "\tseat map %d user %s update %s" \
            % (seat_map_id, row['update_user'], row['update_time'])
    if n==0:
        print "\t not found"

    return seat_map_id


def CheckForDuplicateSeatMaps(conn, acode=None):

    printlog("Flights with duplicate seat maps")

    SmcSql = \
        "SELECT " \
        " fdl.flight_number fn, fdl.flight_date fd, count(*) smc" \
        " FROM flight_seat_map fsm" \
        " JOIN flight_date_leg fdl ON fsm.flight_date_leg_id = fdl.flight_date_leg_id" \
        " WHERE fdl.flight_date > CURRENT" \
        " GROUP BY fdl.flight_number, fdl.flight_date" \
        " HAVING count(*) > 1"

    printlog(SmcSql,2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(SmcSql)

    flights = []
    for row in cur:
        printlog("\t%s %s %s" % (row['fn'], row['fd'], row['smc']))
        flight_number = str(row['fn'])
        flight_date = ReadDate(str(row['fd']))
        flight = ReadFlight(conn, flight_number, flight_date)
        if flight is None:
            print "No information for flight %s depart %s" \
                % (flight_number, flight_date.strftime("%Y-%m-%d"))
        else:
            if acode is None:
                flights.append(flight)
            else:
                if flight.aircraft_code == acode:
                    flights.append(flight)

    return flights


def CheckFlightForDuplicateSeatMaps(conn, flight, aircraft_desc, seat_map_id=None):

    flightNum = flight.flight_number
    fltDate = flight.board_dts
    aircraft_code = flight.aircraft_code

    printlog("Check seat maps for flight %s date %s aircraft description %s" \
        % (flightNum, fltDate.strftime("%Y-%m-%d"), aircraft_code), 1)

    SmcSql = \
        "SELECT count(*) smcount FROM flight_seat_map fsm" \
        " JOIN flight_date_leg fdl ON" \
        "  fsm.flight_date_leg_id = fdl.flight_date_leg_id" \
        " WHERE fdl.flight_number = '%s'" \
        "  AND fdl.flight_date = '%s'" \
            % (flightNum, fltDate.strftime("%m/%d/%Y"))

    printlog(SmcSql,2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(SmcSql)
    flights = []
    FlightDateLegId = 0
    SeatMapId = 0
    SeatMapCount = None
    for row in cur:
        SeatMapCount = int(row['smcount'])

    if SeatMapCount is None:
        printlog("Could not read seat maps for flight %s date %s" \
            % (flightNum, fltDate.strftime("%Y-%m-%d")), 1)
        SeatMapCount = 0
    elif SeatMapCount > 1:
        Smc2Sql = \
            "SELECT fdl.flight_number fnum, fdl.flight_date fdate," \
            "sm.description fdesc,fdl.flight_date_leg_id fldid," \
            "fsm.seat_map_id fsmid" \
            " FROM flight_seat_map fsm" \
            "  JOIN flight_date_leg fdl" \
            "   ON fsm.flight_date_leg_id = fdl.flight_date_leg_id" \
            "  JOIN seat_map sm ON fsm.seat_map_id = sm.seat_map_id" \
            " WHERE fdl.flight_number = '%s' AND fdl.flight_date = '%s'" \
                % (flightNum, fltDate.strftime("%m/%d/%Y"))
        printlog(Smc2Sql, 2)
        cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur2.execute("set isolation dirty read")
        cur2.execute(Smc2Sql)
        for row in cur2:
            fdlid = int(row['fldid'] or 0)
            smid = int(row['fsmid'] or 0)
            printlog("\nFlight  %s date %s" \
                % (flightNum, fltDate.strftime("%Y-%m-%d")), 1)
            printlog("\tflight date leg %s seat map %d aircraft code description '%s'" \
                % (fdlid, smid, row['fdesc']), 1)
            if aircraft_desc is not None:
                if row['fdesc'] == aircraft_desc:
                    FlightDateLegId = fdlid
                    SeatMapId = smid
            elif seat_map_id is not None:
                # Check this seat map ID
                smid = int(row['fsmid'])
                if smid == seat_map_id:
                    FlightDateLegId = fdlid
                    SeatMapId = smid
            else:
                # Nothing to do
                pass

        printlog("Found %d seat maps for flight %s date %s" \
            % (SeatMapCount, flightNum, fltDate.strftime("%Y-%m-%d")), 1)
        if FlightDateLegId:
            printlog("\t matched aircraft description %s" % aircraft_desc, 1)
    elif SeatMapCount == 1:
        pass
    elif SeatMapCount == 0:
        pass
    else:
        print "Invalid number of seat maps (%d) for flight %6s date %s leg %d" \
            % (SeatMapCount, flightNum, fltDate.strftime("%Y-%m-%d"),
               int(row['fldid'] or 0))
    print
    return FlightDateLegId, SeatMapId


def CheckSeatMaps(conn, flight):

    try:
        flightNum = flight.flight_number
        fltDate = flight.board_dts
        aircraft_code = flight.aircraft_code
    except AttributeError:
        return 0

    printlog("Check flight %s seat maps for date %s aircraft code %s" \
        % (flightNum, fltDate.strftime("%Y-%m-%d"), aircraft_code))

    SmcSql = \
        "SELECT count(*) smcount FROM flight_seat_map fsm" \
        " JOIN flight_date_leg fdl ON" \
        "  fsm.flight_date_leg_id = fdl.flight_date_leg_id" \
        " WHERE fdl.flight_number = '%s'" \
        "  AND fdl.flight_date = '%s'" \
            % (flightNum, fltDate.strftime("%m/%d/%Y"))

    printlog(SmcSql,2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(SmcSql)
    flights = []
    SeatMapCount = None
    for row in cur:
        SeatMapCount = int(row['smcount'])

    if SeatMapCount is None:
        print "Could not read seat maps for flight %s date %s" \
            % (flightNum, fltDate.strftime("%Y-%m-%d"))
    elif SeatMapCount > 1:
        print "Found %d seat maps for flight %s date %s aircraft code %s" \
            % (SeatMapCount, flightNum, fltDate.strftime("%Y-%m-%d"), aircraft_code)
        Smc2Sql = \
            "SELECT fdl.flight_number fnum, fdl.flight_date fdate," \
            "sm.description fdesc,fdl.flight_date_leg_id fldid," \
            "fsm.seat_map_id fsmid" \
            " FROM flight_seat_map fsm" \
            "  JOIN flight_date_leg fdl" \
            "   ON fsm.flight_date_leg_id = fdl.flight_date_leg_id" \
            "  JOIN seat_map sm ON fsm.seat_map_id = sm.seat_map_id" \
            " WHERE fdl.flight_number = '%s' AND fdl.flight_date = '%s'" \
                % (flightNum, fltDate.strftime("%m/%d/%Y"))
        printlog(Smc2Sql, 2)
        cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur2.execute("set isolation dirty read")
        cur2.execute(Smc2Sql)
        for row in cur2:
            print "\tflight date leg id %s seat map id %s aircraft description '%s'" \
                % (int(row['fldid'] or 0), row['fsmid'], row['fdesc'])
    elif SeatMapCount == 1:
        Smc2Sql = \
            "SELECT fdl.flight_number fnum,fdl.flight_date fdate," \
            "sm.description fdesc,fdl.flight_date_leg_id fldid" \
            " FROM flight_seat_map fsm" \
            "  JOIN flight_date_leg fdl" \
            "   ON fsm.flight_date_leg_id = fdl.flight_date_leg_id" \
            "  JOIN seat_map sm on fsm.seat_map_id = sm.seat_map_id" \
            " WHERE fdl.flight_number = '%s' and fdl.flight_date = '%s'" \
                % (flightNum, fltDate.strftime("%m/%d/%Y"))
        printlog(Smc2Sql, 2)
        cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur2.execute("set isolation dirty read")
        cur2.execute(Smc2Sql)
        aircraft_code = None
        fdesc = ''
        for row in cur2:
            if row['fdesc'] == '733':
                aircraft_code = '733'
            else:
                aircraft_code = '738'
            fdesc = row['fdesc']
        if aircraft_code is None:
            print "No aircraft code"
            pass
        elif aircraft_code == flight.aircraft_code:
            print "Seat map OK for flight %6s date %s leg %d aircraft code %s (description %s)" \
                % (flightNum, fltDate.strftime("%Y-%m-%d"), int(row['fldid'] or 0),
                   aircraft_code, fdesc)
        else:
            print "Seat map description %s for flight %6s date %s leg %d" \
                  " does not match aircraft code '%s'" \
                % (fdesc, flightNum, fltDate.strftime("%Y-%m-%d"), int(row['fldid'] or 0),
                   flight.aircraft_code)
    elif SeatMapCount == 0:
        print "No seat map for flight %6s date %s" \
            % (flightNum, fltDate.strftime("%Y-%m-%d"))
    else:
        print "Invalid number of seat maps (%d) for flight %6s date %s leg %d" \
            % (SeatMapCount, flightNum, fltDate.strftime("%Y-%m-%d"),
               int(row['fldid'] or 0))
    #print
    return SeatMapCount


def DeleteSeatMap(conn, flight, FlightLegId, MapId, do_del=False):

    printlog("Delete seat map entry for flight %6s depart %s" \
          " (flight date leg %d and seat map %d)" \
        % (flight.flight_number, flight.board_date_iso, FlightLegId , MapId), 1)
    SmcSql = \
        "SELECT count(*) fsm FROM flight_seat_map" \
        " WHERE flight_date_leg_id = %d AND seat_map_id = %d" \
            % (FlightLegId, MapId)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(SmcSql)
    SeatMapCount = 0
    for row in cur:
        SeatMapCount = int(row['fsm'])

    if SeatMapCount <= 0:
        print "Nothing to delete for flight %6s depart %s" \
          " (flight date leg %d and seat map %d)" \
        % (flight.flight_number, flight.board_date_iso, FlightLegId, MapId)
        return
    print "Delete %d seat map entry for flight %6s depart %s" \
          " (flight date leg %d and seat map %d)" \
        % (SeatMapCount, flight.flight_number, flight.board_date_iso, FlightLegId , MapId)

    SmcSql = \
        "DELETE FROM flight_seat_map" \
        " WHERE flight_date_leg_id = %d AND seat_map_id = %d" \
            % (FlightLegId, MapId)
    print "%s;" % SmcSql

    if do_del:
        cur2 = conn.cursor()
        cur2.execute(SmcSql)
        print "Deleted seat map with flight date leg %d and seat map %d" \
            % (FlightLegId , MapId)
        cur2.close()


def RemoveSeatMap(conn, flight, FlightLegId, MapId, do_del=False):

    print "Remove seat map for flight leg ID %d seat map ID %d" \
        % (FlightLegId, MapId)

    if MapId is None:
        print "Could not find flight %6s depart %s" \
            % (flightNum, flight.board_dts.strftime("%Y-%m-%d"))
        return

    flight_numbers, flight_dates = ReadFlightDateLegId(conn, FlightLegId)
    i = 0
    for flight_number in flight_numbers:
        flightNum = flight_number
        flight_date = ReadDate(str(flight_dates[i])).strftime("%Y-%m-%d")
        print "Flight %s depart %s" % (flight_number, flight_date)
        i += 1
    if i == 0:
        print "Flight map %d not found" % FlightLegId
        return

    if flight.flight_number != flightNum or flight.board_date_iso != flight_date:
        print "Flight map %d does not match flight %s depart %s" \
            % (FlightLegId, flight.flight_number, flight.board_date_iso)
        return

    print "Delete flight %6s depart %s" \
          " (flight date leg_id %d and seat map id %d)" \
        % (flightNum, flight_date, FlightLegId , MapId)
    DeleteSeatMap(conn, flight, FlightLegId , MapId, do_del)


def RemoveDuplicateSeatMaps(conn, flight, do_del=False):

    flightNum = flight.flight_number
    fltDate = flight.board_dts.strftime("%m/%d/%Y")
    SmcSql = \
        "SELECT fdl.flight_number fnum,fdl.flight_date fdate," \
        "sm.description fdesc,fdl.flight_date_leg_id fldid," \
        "fsm.seat_map_id fsmid" \
        " FROM flight_seat_map fsm" \
        "  JOIN flight_date_leg fdl" \
        "   ON fsm.flight_date_leg_id = fdl.flight_date_leg_id" \
        "  JOIN seat_map sm on fsm.seat_map_id = sm.seat_map_id" \
        " WHERE fdl.flight_number = '%s' AND fdl.flight_date = '%s'" \
            % (flightNum, fltDate)
    printlog(SmcSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(SmcSql)

    FlightLegId = None
    MapId = None
    for row in cur:
        FlightLegId = int(row['fldid'])
        print "\tflight date leg id %s seat map id %s (%s)" \
            % (FlightLegId, row['fsmid'], row['fdesc'])
        if row['fdesc'] == '733':
            aircraft_code = '733'
        else:
            aircraft_code = '738'
        if aircraft_code == flight.aircraft_code:
            MapId = int(row['fsmid'])

    if not MapId:
        print "Could not find flight %6s date %s with aircraft code %s" \
            % (flightNum, flight.board_dts.strftime("%Y-%m-%d"),
               flight.aircraft_code)
        return

    print "Delete flight %6s date %s with aircraft code %d" \
          " (flight date leg_id %d and seat map id %d)" \
        % (flightNum, flight.board_dts.strftime("%Y-%m-%d"), aircraft_code,
           FlightLegId , MapId)
    SmcSql = \
        "DELETE FROM flight_seat_map" \
        " WHERE flight_date_leg_id = %d AND seat_map_id = %d" \
            % (FlightLegId , MapId)
    print "%s" % SmcSql

    if do_del:
        cur = conn.cursor()
        cur.execute(SmcSql)
        cur.close()
        print "Deleted seat map with flight date leg %d and seat map %d" \
            % (FlightLegId , MapId)


def ReadAircraftConfig(conn, config_table):

    print "Configuration table for config table '%s' [aircraft_config] :" % config_table
    SmcSql = \
        "SELECT config_table,aircraft_code,seat_capacity,selling_class,update_time,update_user" \
        " FROM aircraft_config " \
        " WHERE config_table = '%s'" \
            % config_table
    printlog(SmcSql,2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(SmcSql)

    n = 0
    for row in cur:
        n += 1
        print "\tconfig %4s aircraft %4s seats %3s class %s user %s update %s" \
            % (row['config_table'], row['aircraft_code'],
               row['seat_capacity'], row['selling_class'],
               row['update_user'], row['update_time'])
    if n == 0:
        print "\tnot found"


def GetConfigTableNo(conn, aircraft_code):

    print "Configuration table for aircraft code '%s' [aircraft_config] :" % aircraft_code
    SmcSql = \
        "SELECT config_table,aircraft_code,seat_capacity,selling_class,update_time,update_user" \
        " FROM aircraft_config " \
        " WHERE aircraft_code = '%s'" \
            % aircraft_code
    printlog(SmcSql,2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(SmcSql)

    n = 0
    for row in cur:
        n += 1
        print "\tConfig %4s aircraft %4s seats %3s class %1s user %-5s update %s" \
            % (row['config_table'], row['aircraft_code'],
               row['seat_capacity'], row['selling_class'],
               row['update_user'], row['update_time'])
    if n == 0:
        print "\tnot found"


def ReadFLightSeatMapId(conn, seat_map_id):

    print "Seat map for seat map ID %d [seat_map]" % seat_map_id
    FdSql = "select description,update_time,update_user from seat_map where seat_map_id='%d'" \
        % (seat_map_id)
    printlog(FdSql,2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(FdSql)
    n = 0
    aircraft_desc = ''
    for row in cur:
        n += 1
        aircraft_desc = row['description']
        print "\tdescription '%s' user %s update %s" \
            % (aircraft_desc, row['update_user'], row['update_time'])
    if n == 0:
        print "\tnot found"

    return n, aircraft_desc


def ReadSeatMapClass(conn, seat_map_id):

    print "Seat map class for seat map ID %d [seat_map_class]" % seat_map_id
    FdSql = "select selling_class,update_time,update_user from seat_map_class where seat_map_id='%d'" \
        % (seat_map_id)
    printlog(FdSql,2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(FdSql)
    n = 0
    selling_class = ''
    for row in cur:
        n += 1
        selling_class = row['selling_class']
        print "\tselling class '%s' user %s update %s" \
            % (selling_class, row['update_user'], row['update_time'])
    if n == 0:
        print "\tnot found"

    return n, selling_class


def ReadSeatDefinition(conn, seat_map_id):

    print "Seat definition for seat map ID %d [seat_definition]" % seat_map_id

    FdSql = \
        "SELECT seat_definition_id,seat_code,update_time,update_user" \
        " FROM seat_definition WHERE seat_map_id=%d" \
            % (seat_map_id)
    printlog(FdSql,2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(FdSql)
    n = 0
    selling_class = ''
    for row in cur:
        n += 1
        print "\tdefinition %d code %s user %s date %s" \
            % (row['seat_definition_id'], row['seat_code'], \
               row['update_user'], row['update_user'])
    if n == 0:
        print "\tnot found"

def ReadSeatMapId(conn, seatnum):

    print "Seat map ID for %s [seat_definition]" % seatnum
    if len(seatnum) == 2:
        row_number = int(seatnum[0])
        seat_code = seatnum[1]
    elif len(seatnum) == 2:
        row_number = int(seatnum[0:2])
        seat_code = seatnum[2:]

    FdSql = \
        "SELECT seat_definition_id FROM seat_definition" \
        " WHERE row_number=%d AND seat_code='%s'" \
            % (row_number, seat_code)
    printlog(FdSql,2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(FdSql)
    n = 0
    for row in cur:
        n += 1
        print "\t%s" % row['seat_definition_id']
    if n == 0:
        print "\tnot found"

    return n
