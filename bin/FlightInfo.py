#!/usr/bin/python3 -B
#
# Python won't try to write .pyc or .pyo files on the import of source modules
#
# @file FlightInfo.py
#
"""
Provide flight information.
"""

import os
import sys
import getopt
from configobj import ConfigObj
from xml.dom import minidom
import psycopg2
from datetime import datetime, timedelta, datetime

from BarsConfig import BarsConfig
from BarsLog import set_verbose, printlog
from ReadDateTime import ReadDate, ReadTime
#from MangoBanner import print_banner
from Booking.ReadSeatReservation import ReadSeatReservation
#from ReadSeatReservation import ReadReserveSeats, ReadFlightDateLegInfo, \
                                #ReadSeatReservation, \
                                #CheckSeatReservation, ReadSeatDefinition, \
                                #FlightSeatBookings
#from ReadFlightSeats import ReadFlightSeats, ShowFlightSeats, \
                            #ReadReleaseSeats, ReleaseSeat, CheckReleaseSeats, \
                            #ReadBookSeatReservations, CheckReserveSeats, \
                            #ReadFlightDateLegId, ReadFlightDateAllSeats, \
                            #ReadFlightDateLeg
# from ReadFlightDateLegs import ReadFlightDateLegId
from Flight.ReadFlights import ReadFlightSegmDates, ReadFlightSegmDate, \
                        ReadDeparture, \
                        ReadFlights, ReadFlightsDate, \
                        ReadFlightDateClassSeatMaps, ReadCodeShare, \
                        SetCodeShare, ReadFlightDeparture, \
                        CheckFlightDateClassSeatMaps, ReadFlight, \
                        ReadFlightInformation, GetFlightDataSsm, GetFlights, \
                        ReadFlightsDateLeg, CheckFlight
#from FlightReconcile import FlightReconcile, AsrReconcile
#from SystemInfo import ReadSystemSettingInfo
#from ReadItenaries import ReadBookingItenary
#from ReadBookingRef import ReadLocator
from Flight.ReadFlightPeriods import ReadFlightPeriodsGui, ReadFlightPeriods, \
                              ReadFlightPeriodsDate, ReadTestPeriods, \
                              ReadFlightPerdLegs, ReadFlightPerdCls, \
                              ReadFlightPerdSegCls, ReadFlightPerdSegm, \
                              ReadFlightPerdPrnt, ReadSchdChngAction, \
                              ReadTestInventrySegm, ReadTestPerdSegm, \
                              ReadTestPerdCls, ReadTestPerdPrnt
from Flight.FlightData import FlightData
#
#from GetSeatMap import GetSeatMap, GetFlightDetail, GetFlightDetails
#from GetSeatData import GetFlightDateClassSeatMaps
from Flight.ReadSeatMap import ReadFlightSeatMap, \
                        GetConfigTableNo, ReadSeatMapConfiguration, \
                        ReadFLightSeatMapId, ReadSeatMapId
#from ReadFareRoute import ReadFareRouteIds, ReadFareRoutes, \
                          #ReadFareRoutesDate, ReadFareRouteBranches, \
                          #ReadFareRouteCompanies, ReadFareRouteDesignators, \
                          #ReadFareAgencies
from Flight.ReadSchedPeriod import ReadSchedPeriod, ReadConfigNumberOfSeats, \
                            ReadFlightPeriods, ReadFlightPeriodsLatest
#from ReadFlightBookings import ReadFlightBookings, ReadFlightContacts, \
                               #ReadFlightPaxNames
from Ssm.ReadSsmData import ReadSsmFlightData, ReadSsmBookData, ReadSsmTim
from Flight.ReadFlightLegs import ReadFlightSharedLeg, ReadFlightDateLegs, \
                           ReadtestPeriodLegs, ReadAsrReconcileHistory
from Ssm.ReadAircraftConfig import ReadAircraftConfig
#from CheckAvailability import CheckAvailability
from Flight.ReadFlightSegments import ReadSegmentStatus, ReadFlightPax
from Flight.ReadFlightTimes import ReadFlightTimes, ReadFlightPerdLegsTimes, \
                            ReadFlightSegmDateTimes, ReadFlightSegmDates, \
                            ReadFlightDateLegTimes, ReadFlightSharedLegTimes
from DbConnect import OpenDb, CloseDb
from BarsBanner import print_banner


def read_flight_stuff(conn, flight_number, dt1, selling_cls, seat_number):

    print("__________________________________")
    print("Flight %s board %s stuff" % (flight_number, dt1.strftime("%Y-%m-%d")))
    CheckFlight(conn, flight_number, dt1)
    print("_____________________________")
    flight_date_leg_ids = ReadFlightDateLegs(conn, flight_number, dt1)
    print("____________________")
    aircraft_codes, config_table_nos = ReadFlightSharedLeg(conn, flight_number, dt1)
    for fdlid in flight_date_leg_ids:
        print("____________________")
        print("Flight date leg ID %d" % fdlid)
        ReadAsrReconcileHistory(conn, fdlid)
        smid = ReadFlightSeatMap(conn, fdlid)
        ReadFLightSeatMapId(conn, smid)
        ReadSeatMapConfiguration(conn, fdlid, None)
    if seat_number is not None:
        print("____________________")
        ReadSeatReservation(conn, flight_number, dt1, seat_number)
    i = 0
    for aircraft_code in aircraft_codes:
        print("____________________")
        ReadAircraftConfig(conn, aircraft_code, config_table_nos[i], None)
        i += 1
    print("____________________")
    schedule_period_nos = ReadFlightPeriodsDate(conn, flight_number, dt1)
    for schedule_period_no in schedule_period_nos:
        print("_______________________")
        print("Schedule period no %d" % schedule_period_no)
        ReadFlightPerdLegs(conn, flight_number, schedule_period_no)
        ReadFlightPerdSegm(conn, flight_number, schedule_period_no)
        ReadFlightPerdCls(conn, flight_number, schedule_period_no, selling_cls)
        ReadFlightPerdSegCls(conn, flight_number, schedule_period_no, selling_cls)
        ReadFlightPerdPrnt(conn, flight_number, schedule_period_no, selling_cls)
        ReadSchdChngAction(conn, flight_number, schedule_period_no, selling_cls)
        ReadTestPerdSegm(conn, flight_number, schedule_period_no)
        ReadTestPerdCls(conn, flight_number, schedule_period_no, selling_cls)
        ReadTestPerdPrnt(conn, flight_number, schedule_period_no, selling_cls)
        ReadtestPeriodLegs(conn, flight_number, schedule_period_no)
        ReadTestPeriods(conn, flight_number, schedule_period_no, dt1)
        ReadTestInventrySegm(conn, flight_number, schedule_period_no, selling_cls)
    print("____________________")
    ReadFlightInformation(conn, flight_number, dt1)
    ReadSegmentStatus(conn, flight_number, dt1)
    #ReadFlightDateLeg(conn, flight_number, dt1)


#def read_flight_bookings(conn, book_no, seat_number):

    #print("_____________________________"
    #print("Flight bookings for book %8d seat %3s" % (book_no, seat_number)
    #print("_____________________________"
    #n = ReadSeatDefinition(conn, seat_number)
    #if n < 0:
        #return n
    #flight_numbers, flight_dates, selling_classes, flight_reserves = \
        #ReadBookingItenary(conn, book_no)
    #n = 0
    #for flight_number in flight_numbers:
        #dt1 = flight_dates[n]
        #print("Flight %s date %s class %s reserve %s" \
            #% (flight_number, dt1.strftime("%Y-%m-%d"), selling_classes[n],
               #flight_reserves[n])
        #CheckSeatReservation(conn, flight_number, dt1, None, seat_number,
                             #book_no)
        #CheckSeatReservation(conn, flight_number, dt1, None, seat_number)
        #read_flight_stuff(conn, flight_number, dt1, selling_classes[n],
                          #seat_number)
        #print
        #n += 1
    #return n


#def read_code_share(conn, flight_number, board_date, selling_class_code,
                    #departure_airport, arrival_airport, city_pair, company_code='ZZ'):

    #departure_time = None
    #arrival_time = None
    #aircraft_code = None

    #flights = []
    #flights.append(FlightData(selling_class_code, flight_number, board_date,
                   #departure_time, arrival_time, departure_airport, arrival_airport,
                   #city_pair, company_code, aircraft_code))
    #ReadCodeShare(conn, flights[0])


def read_flight_data(conn, flight_number, dt1, company_code='ZZ'):

    n, origin_airport, destination_airport, departure_time = \
        ReadFlightDateLegInfo(conn, flight_number, dt1)
    if n == 0:
        print("Flight %s date %s not found" \
              % (flight_number, dt1.strftime("%Y-%m-%d")))
        sys.exit(1)
    flight = FlightData('Y', flight_number, dt1, departure_time, 0,
                        origin_airport, destination_airport,
                        0, company_code, aircraft_code=None)
    return flight


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def usage(pname='FlightInfo.py'):
    print_banner()
    print("Flights for a booking :")
    print("\t %s -B <BOOKNO>" % pname)
    print("\t %s -L <LOCATOR>" % pname)
    print("Flight details for a date:")
    print("\t %s [-F <FLIGHT>] -D <DATE>" % pname)
    print("\t %s -y [-F <FLIGHT>] -D <DATE>" % pname)
    print("Codeshares :")
    print("\t %s -y --code -D <DATE> [-E <DATE>] [-F <FLIGHT>] [-P <DEPART> -Q <ARRIVE>]"
          % pname)
    print("Class map :")
    print("\t %s --class -F <FLIGHT> -D <DATE>" % pname)
    print("Seat map description :")
    print("\t %s --desc [-F <FLIGHT>] -D <DATE>" % pname)
    print("Check release of seat reservations :")
    print("\t %s --rel -F <FLIGHT> -D <DATE> -S <SEAT>" % pname)
    print("Release seat reservations :")
    print("\t %s [-i] --rel -F <FLIGHT> -D <DATE> -S <SEAT>" % pname)
    print("Seat reservations for a booking :")
    print("\t %s --res -L <LOCATOR>" % pname)
    print("\t %s --res -B <BOOKNO>" % pname)
    print("Seat reservations for a flight :")
    print("\t %s --res -F <FLIGHT> -D <DATE>" % pname)
    print("Passenger contacts for a flight :")
    print("\t %s [-f] --contact -F <FLIGHT> -D <DATE>" % pname)
    print("Seat availability for a flight :")
    print("\t %s --seat -F <FLIGHT> -D <DATE>" % pname)
    print("Seat bookings for a flight :")
    print("\t %s --book -F <FLIGHT> -D <DATE>" % pname)
    print("Test periods :")
    print("\t %s --test -F <FLIGHT>" % pname)
    print("Fare routes :")
    print("\t %s --fare -F <FLIGHT>" % pname)
    print("Check PNL files for flight :")
    print("\t %s --pnl <FLIGHT> -D <DATE>" % pname)
    print("Check reserved seats for flight :")
    print("\t %s -F <FLIGHT> -D <DATE> -S <SEAT>" % pname)
    print("Flight periods :")
    print("\t %s -F <FLIGHT>" % pname)
    print("\t %s -F <FLIGHT> -D <DATE> -N <COUNT>" % pname)
    print("Flight periods as used by MARS GUI :")
    print("\t %s -F <FLIGHT> -R <PERD>" % pname)
    print("Flight periods as used by ASM/SSM processing :")
    print("\t %s --ssm -F <FLIGHT> -K <FREQ> -R <PERD>" % pname)
    print("\t %s --tim -F <FLIGHT> -D <DATE> -E <DATE> [-K <FREQ>]" % pname)
    print("Data for a flight as used by ASM/SSM processing :")
    print("\t %s --ssmdata -F <FLIGHT> -D <DATE> [-E <DATE>]" % pname)
    print("\t %s --ssmbook -F <FLIGHT> -D <DATE> -R <PERD>" % pname)
    print("End transaction check of reserved seats for flight :")
    print("\t %s --et -B <BOOKNO> -F <FLIGHT> -D <DATE> -S <SEAT>" % pname)
    print("\t %s --et -L <LOCATOR> -F <FLIGHT> -D <DATE> -S <SEAT>" % pname)
    print("Check flight availability :")
    print("\t %s --avail -D <DATE> [-E <DATE>]" % pname)
    print("Check flight reconcile :")
    print("\t %s --recon -D <DATE> [-E <DATE>]" % pname)
    print("Configuration for aircraft code :")
    print("\t %s -A <AIRCRAFT> [-C <CLASS>] [-N <COUNT>]" % pname)
    print("Configuration for config table :")
    print("\t %s -T <CFG> [-C <CLASS>] [-N <COUNT>]" % pname)
    print("Run flight reconcile :")
    print("\t %s --recon -D <DATE> -N <COUNT>" % pname)
    print("\t %s --recon -F <FLIGHT> -D <DATE>" % pname)
    print("Configuration table for aircraft code :")
    print("\t %s --cfg -A <AIRCRAFT>" % pname)
    print("Check flight times")
    print("\t %s --time -F <FLIGHT> -D <DATE>" % pname)
    print("Check flight bookings")
    print("\t %s --time -x -F <FLIGHT> -D <DATE>" % pname)
    print("\nParameters:")
    print("\t -A <AIRCRAFT>\t aircraft code")
    print("\t -B <BOOKNO>\t booking number")
    print("\t -C <CLASS>\t selling class")
    print("\t -D <DATE>\t board date")
    print("\t -E <DATE>\t end date")
    print("\t -F <FLIGHT>\t flight number")
    print("\t -I <LEG>\t flight leg ID")
    print("\t -K <FREQ>\t flight frequency days (1=Monday) e.g. 1-2-4-6-")
    print("\t -L <LOCATOR>\t locator, e.g. PNRWYY")
    print("\t -M <MAP>\t seat map ID")
    print("\t -N <COUNT>\t number of seats or days")
    print("\t -P <CITY>\t departure airport")
    print("\t -Q <CITY>\t arrival airport")
    print("\t -R <PERD>\t schedule period number")
    print("\t -S <SEAT>\t seat numbers as comma seperated list")
    print("\t -T <CFG>\t configuration table number")
    print("\t -X <TIME>\t departure time")
    print("\t -Y <TIME>\t arrival time")
    sys.exit(1)


# Pythonic entry point
def main(argv):
    barsdir = os.environ['BARSDIR']
    etcdir = "%s/etc" % barsdir
    flight_number = None
    dt1 = None
    dt2 = None
    arrival_time = 0
    departure_time = 0
    schedule_period_no = 0
    recCount = 0
    seat_map_id = None
    flight_date_leg_id = 0

    chkit = False
    fare_route = False
    test_periods = False
    reserve_seat = False
    seat_all = False
    release_seat = False
    seat_book = False
    et_asr = False
    desc_map = False
    list_flights = False
    seatmapid_read = False
    csflag = False
    update_db = False
    asm_ssm = False
    cfg_table = False
    pax_book = False
    contact_pax = False
    force_query = False
    ssm_data = False
    ssm_book = False
    ssm_tim = False
    flt_recon = False
    pnl_file = False
    chk_avail = False
    chk_ftimes = False
    chk_perd = False
    list_csv = False
    list_pax = False

    seat_numbers = []
    selling_cls = None
    departure_airport = None
    arrival_airport = None
    aircraft_code = None
    config_table = None
    locator = None
    book_no = None
    frequency_code = None
    selling_class_code='Y'
    company_code='ZZ'
    rval = 0
    files = []

    #pdb.set_trace()

    if len(argv) < 1:
        usage()

    try:
        opts, args = getopt.getopt(argv,
                                   "cfhivxyV"
                                   "A:B:C:D:E:F:I:K:L:M:N:P:Q:R:S:T:X:Y:",
                                   ["help", "date=", "edate=", "flight=",
                                    "period=", "seats=", "days=", "class=",
                                    "locator=", "bookno=",
                                    "depart=", "arrive=",
                                    "aircraft=", "freq=", "cfgtable=",
                                    "et", 'fare', 'desc',
                                    'res', 'seat', 'book', 'rel',
                                    'test', 'pax', 'smid', 'recon',
                                    'code', 'ssm', 'tim',  'cfg', 'contact',
                                    'ssmdata', 'pnl',
                                    'ssmbook', 'avail', 'time', 'csv', 'perd'])
    except getopt.GetoptError:
        print("Error in options")
        #usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            usage()
        elif opt == '-c':
            chkit = True
        elif opt == '-v':
            # Debug output
            set_verbose(1)
        elif opt == '--avail':
            chk_avail = True
        elif opt == '--cfg':
            cfg_table = True
        elif opt == '--class':
            class_map = True
        elif opt == '--et':
            et_asr = True
        elif opt == '--pnl':
            pnl_file = True
        elif opt == '--fare':
            fare_route = True
        elif opt == '-f':
            force_query = True
        elif opt == '-i':
            update_db = True
        elif opt == '--desc':
            desc_map = True
        elif opt == '--rel':
            release_seat = True
        elif opt == '--res':
            reserve_seat = True
        elif opt == '--seat':
            seat_all = True
        elif opt == '--book':
            seat_book = True
        elif opt == '--csv':
            list_csv = True
        elif opt == '--contact':
            contact_pax = True
        elif opt == '--pax':
            pax_book = True
        elif opt == '--perd':
            chk_perd = True
        elif opt == '--recon':
            flt_recon = True
        elif opt == '--test':
            test_periods = True
        elif opt == '--code':
            csflag = True
        elif opt == '--smid':
            seatmapid_read = True
        elif opt == '--ssm':
            asm_ssm = True
        elif opt == '--ssmdata':
            ssm_data = True
        elif opt == '--tim':
            ssm_tim = True
        elif opt == '--time':
            chk_ftimes = True
        elif opt == '--ssmbook':
            ssm_book = True
        elif opt == '-x':
            list_pax = True
        elif opt == '-y':
            list_flights = True
        elif opt == "-A" or opt == "--aircraft":
            aircraft_code = str(arg).upper()
            printlog(1, "\t aircraft code %s" % aircraft_code)
        elif opt in ("-B", "--bookno"):
            book_no = int(arg)
        elif opt in ("-C", "--class"):
            selling_cls = str(arg).upper()
        elif opt in ("-D", "--date"):
            dt1 = ReadDate(arg)
            printlog(1, "\t flight date %s" % dt1.strftime("%Y-%m-%d"))
        elif opt in ("-E", "--edate"):
            dt2 = ReadDate(arg)
        elif opt in ("-F", "--flight"):
            if '/' in arg:
                fndata = arg.split('/')
                flight_number = fndata[0]
                dt1 = ReadDate(fndata[1])
            else:
                flight_number = arg
        elif opt == "-I":
            flight_date_leg_id = int(arg)
            printlog(2, "\t flight_date_leg_id %d" % flight_date_leg_id)
        elif opt in ("-L", "--locator"):
            locator = str(arg).upper()
        elif opt in ("-K", "--freq"):
            frequency_code = arg
        elif opt == "-M":
            seat_map_id = int(arg)
            printlog(2, "\t seat_map_id %d" % seat_map_id)
        elif opt in ("-N", "--days"):
            recCount = int(arg)
            printlog(1, "\t count %d" % recCount)
        elif opt in ("-P", "--depart"):
            departure_airport = str(arg).upper()
            printlog(1, "\t depart %s" % departure_airport)
        elif opt in ("-Q", "--arrive"):
            arrival_airport = str(arg).upper()
            printlog(1, "\t arrive %s" % arrival_airport)
        elif opt in ("-R", "--period"):
            schedule_period_no = int(arg)
        elif opt in ("-S", "--seats"):
            seat_numbers = str(arg).upper().split(',')
        elif opt in ("-T", "--cfgtable"):
            config_table = str(arg).upper()
        elif opt == "-X":
            departure_time = ReadTime(arg)
        elif opt == "-Y":
            arrival_time = ReadTime(arg)
        elif opt == '-V':
            # Debug output
            set_verbose(2)
        else:
            print("Unknown option %s" % opt)
            return 1

    for arg in args:
        files.append(arg.strip())

    # Check for invalid combined options
    if list_flights:
        if desc_map:
           print("Cannot combine list flight with other options")
           return 1
        elif book_no is not None or locator is not None:
           print("Cannot list flights for a booking")
           return 1
    elif desc_map:
        if list_flights or csflag:
           print("Cannot combine map description with other options")
           return 1
        elif book_no is not None or locator is not None:
           print("Cannot list map description for a booking")
           return 1
    elif csflag:
        if desc_map:
           print("Cannot combine code share with other options")
           return 1
        elif book_no is not None or locator is not None:
           print("Cannot list code shares for a booking")
           return 1

    cfg = BarsConfig('%s/bars.cfg' % etcdir)

    # Open connection to database
    conn = OpenDb(cfg.dbname, cfg.dbuser, cfg.dbhost)

    reconcile_window = 0 # int(ReadSystemSettingInfo(conn, "RECONCILE_WINDOW"))

    # No flight number specified
    if cfg_table and aircraft_code is not None:
        printlog(2, "Get config table for aircraft code %s" % aircraft_code)
        GetConfigTableNo(conn, aircraft_code)
    elif config_table is not None:
        ReadAircraftConfig(conn, None, config_table, selling_cls, recCount)
    elif chk_perd and dt1 is not None and dt2 is not None:
        fperds = ReadFlightPeriods(conn, flight_number, dt1, dt2)
        for fperd in fperds:
            fperd.display(list_csv)
    elif chk_perd:
        fperds = ReadFlightPeriodsLatest(conn, flight_number, dt1, dt2)
        for fperd in fperds:
            fperd.display(list_csv)
    elif flight_number is None:
        if list_flights and dt1 is not None:
            if dt2 is not None:
                printlog(2, "List flights from %s to %s"
                         % (dt1.strftime("%Y-%m-%d"), dt2.strftime("%Y-%m-%d")))
                for single_date in daterange(dt1, dt2):
                    flights = ReadFlightsDate(conn, single_date, recCount,
                                              departure_airport,
                                              arrival_airport,
                                              code_share=csflag)
                    for flight in flights:
                        SetCodeShare(conn, flight)
                        flight.display()
                    #print
            else:
                printlog(2, "List flights for %s" % dt1.strftime("%Y-%m-%d"))
                flights = ReadFlightsDate(conn, dt1, recCount,
                                          departure_airport, arrival_airport,
                                          code_share=csflag)
                for flight in flights:
                    SetCodeShare(conn, flight)
                    flight.display()
        # elif chk_avail and dt1 is not None and departure_airport is not None and arrival_airport is not None:
            # CheckAvailability(conn, dt1, departure_airport, arrival_airport, company_code)
        elif flt_recon and recCount and dt1 is not None:
            FlightReconcile(conn, dt1, recCount)
            return
        elif fare_route and dt1 is not None:
            ReadFareRoutesDate(conn, dt1)
        elif reserve_seat and (book_no is not None or locator is not None):
            if book_no is None:
                if locator is None:
                    print("No book number or locator")
                    conn.close()
                    return 1
                book_no = ReadLocator(conn, locator)
            ReadBookSeatReservations(conn, book_no)
        elif chkit and desc_map and dt1 is not None:
            flights = ReadFlightsDate(conn, dt1, recCount, departure_airport,
                                      arrival_airport, code_share=csflag)
            for flight in flights:
               CheckFlightDateClassSeatMaps(conn, flight)
        elif desc_map and dt1 is not None:
            flights = ReadFlightsDate(conn, dt1, recCount, departure_airport,
                                      arrival_airport, code_share=csflag)
            for flight in flights:
                ReadFlightDateClassSeatMaps(conn, flight)
        # elif csflag and dt1 is not None:
            # if dt2 is not None:
                # for single_date in daterange(dt1, dt2):
                    ##flights = ReadFlightsDateLeg(conn, single_date, recCount,
                                                 ##departure_airport, arrival_airport)
                    # flights = ReadFlightsDate(conn, single_date, recCount,
                                              # departure_airport, arrival_airport, code_share=csflag)
                    # for flight in flights:
                        # ReadCodeShare(conn, flight)
                    # print
            # else:
                # flights = ReadFlightsDate(conn, dt1, recCount, departure_airport,
                                          # arrival_airport, code_share=csflag)
                # for flight in flights:
                    # ReadCodeShare(conn, flight)
        # elif seatmapid_read:
            # for seat_number in seat_numbers:
                # print("________________________"
                # ReadSeatMapId(conn, seat_number)
        elif book_no is not None:
            for seat_number in seat_numbers:
                print("________________________")
                read_flight_bookings(conn, book_no, seat_number)
        elif locator is not None:
            book_no = ReadLocator(conn, locator)
            for seat_number in seat_numbers:
                print("________________________")
                read_flight_bookings(conn, book_no, seaReadFlightPaxReadFlightPaxt_number)
        elif dt1 is not None and recCount != 0:
            ReadFlightSegmDates(conn, dt1, recCount, reconcile_window)
        elif dt1 is not None and dt2 is not None:
            print("Flights from %s to %s"
                  % (dt1.strftime("%Y-%m-%d"), dt2.strftime("%Y-%m-%d")))
            for single_date in daterange(dt1, dt2):
                flights = ReadFlightsDate(conn, single_date, recCount,
                                          departure_airport, arrival_airport,
                                          code_share=csflag)
                for flight in flights:
                    flight.display()
        elif dt1 is not None:
            flights = ReadFlightsDate(conn, dt1, recCount, departure_airport,
                                      arrival_airport, code_share=csflag)
            for flight in flights:
                if list_csv:
                    flight.displaycsv()
                else:
                    flight.display()
        else:
            print("No flight number")

    elif not asm_ssm and aircraft_code is not None:
        ReadAircraftConfig(conn, aircraft_code, None, selling_cls, recCount)
    # Flight number specified
    else:
        city_pair = 0
        if list_pax and dt1 is not None:
            ReadFlightPax(conn, flight_number, dt1)
            return 0
        elif not fare_route and dt1 is not None and dt2 is not None:
            printlog(2, "Read flight %s from %s to %s"
                     % (flight_number, dt1.strftime("%Y-%m-%d"),
                        dt2.strftime("%Y-%m-%d")))
            n = 0
            for single_date in daterange(dt1, dt2):
                n, flights = \
                    ReadDeparture(conn, cfg.CompanyCode, cfg.SellingClasses[0],
                                  flight_number, single_date)
                departure_airport = flights[0].departure_airport
                arrival_airport = flights[0].departure_airport
                city_pair = flights[0].city_pair
            if n != 1:
                print("Could not read departures and arrivals" \
                      " for flight %s board %s" \
                      % (flight_number, dt1.strftime("%Y-%m-%d")))
                if not force_query:
                    conn.close()
                    return 1
        elif not fare_route and dt1 is not None:
            n, flights = \
                ReadDeparture(conn, cfg.CompanyCode, cfg.SellingClasses[0],
                              flight_number, dt1)
            if n != 1:
                print("Could not read departures and arrivals" \
                      " for flight %s board %s" \
                      % (flight_number, dt1.strftime("%Y-%m-%d")))
                if not force_query:
                    conn.close()
                    return 1
            departure_airport = flights[0].departure_airport
            arrival_airport = flights[0].departure_airport
            city_pair = flights[0].city_pair
        if city_pair == 0:
            printlog(1, "City pair not found", 1)
        printlog(1, "Depart %s arrive %s city pair %d"
                 % (departure_airport, arrival_airport, int(city_pair)))

        if chk_ftimes and dt1 is not None and dt2 is None:
            flight = FlightData('Y', flight_number, dt1,
                                departure_time, arrival_time,
                                departure_airport, arrival_airport, 0,
                                'X', 'X',
                                company_code, aircraft_code)
            schedule_period_no, start_date, end_date = \
                ReadFlightTimes(conn, flight)
            ReadFlightPerdLegsTimes(conn, flight, schedule_period_no)
            ReadFlightSegmDateTimes(conn, flight, schedule_period_no)
            flight_dates = ReadFlightSegmDates(conn, flight, schedule_period_no)
            ReadFlightDateLegTimes(conn, flight, flight_dates)
            ReadFlightSharedLegTimes(conn, flight, flight_dates)
        elif pnl_file and dt1 is not None:
            pax_names = []
            print("Read PNL files:")
            for filename in files:
                print("Read PNL file %s" % filename)
                with open(filename) as f:
                    lines = f.readlines()
                for line in lines:
                    if line[0] != '1':
                        continue
                    toks = line[1:].split(' ')
                    pax_name = toks[0].rstrip()
                    printlog(1, "%s" % pax_name, 1)
                    pax_names.append(pax_name)
            n_pax_names = len(pax_names)
            print("Found %d passenger records in files" % n_pax_names)
            flight = FlightData('Y', flight_number, dt1,
                                departure_time, arrival_time,
                                departure_airport, arrival_airport, 0,
                                'X', 'X',
                                company_code, aircraft_code)
            pax_books = ReadFlightPaxNames(conn, flight)
            n_pax_books = len(pax_books)
            print("Found %d passenger bookings in database" % n_pax_books)
            if n_pax_books <= n_pax_names:
                n = 0
                for pax_name in pax_names:
                    if pax_name in pax_books:
                        print("Found pax %s in bookings" % pax_name)
                        n += 1
                    else:
                        print("Pax %s not found in bookings" % pax_name)
            else:
                n = 0
                for pax_book in pax_books:
                    if pax_name in pax_names:
                        print("Found pax %s (%d) in files"
                              % (pax_book, pax_books[pax_book]))
                        n += 1
                    else:
                        print("Pax %s (%d) not found in files"
                              % (pax_book, pax_books[pax_book]))
            print("Matched %d records" % n)
        elif ssm_tim and dt1 is not None and dt2 is not None:
            n, flights = \
                ReadDeparture(conn, cfg.CompanyCode, cfg.SellingClasses[0],
                              flight_number, dt1)
            if n != 1:
                print("Could not read departures and arrivals" \
                      " for flight %s board %s" \
                      % (flight_number, dt1.strftime("%Y-%m-%d")))
                if not force_query:
                    conn.close()
                    return 1
            n = ReadSsmTim(conn, flights[0], dt1, dt2, frequency_code)
            if n == 0:
                CheckSsmTim(conn, flights[0], sdate, edate, frequency_code, aircraft_code)
        elif flt_recon and dt1 is not None:
            AsrReconcile(conn, flight_number, dt1)
        elif pax_book and dt1 is not None:
            n, flights = \
                ReadDeparture(conn, cfg.CompanyCode, cfg.SellingClasses[0],
                              flight_number, dt1)
            ReadFlightBookings(conn, flights[0])
        elif contact_pax and dt1 is not None:
            n, flights = \
                ReadDeparture(conn, cfg.CompanyCode, cfg.SellingClasses[0],
                              flight_number, dt1)
            ReadFlightContacts(conn, flights[0])
        elif ssm_data and dt1 is not None:
            n, flights = \
                ReadDeparture(conn, cfg.CompanyCode, cfg.SellingClasses[0],
                              flight_number, dt1)
            ReadSsmFlightData(conn, flights[0], dt1)
        elif ssm_book and schedule_period_no is not None and dt1 is not None:
            n, flights = \
                ReadDeparture(conn, cfg.CompanyCode, cfg.SellingClasses[0],
                              flight_number, dt1)
            ReadSsmBookData(conn, flights[0], schedule_period_no)
        elif contact_pax and dt1 is not None:
            flight = ReadFlightPax(conn, flight_number, dt1)
        elif list_flights:
            flights = ReadFlights(conn, flight_number, dt1, dt2, None, None, code_share=csflag)
            #flights = ReadFlight(conn, flight_number, dt1)
            n = len(flights)
            if n == 0:
                print("Flight %s date %s not found" % (flight_number, dt1))
            else:
                for flight in flights:
                    if list_csv: flight.displaycsv()
                    else: flight.display()
            # print("Found %d flights" % n)
        elif fare_route and dt1 is not None:
            n, fare_route_ids = ReadFareRouteIds(conn, flight_number)
            for fare_route_id in fare_route_ids:
                # print("Fare route ID %s date %s" % fare_route_id)
                ReadFareRoutesDate(conn, dt1, fare_route_id)
                ReadFareRouteBranches(conn, fare_route_id)
                ReadFareRouteCompanies(conn, fare_route_id)
                ReadFareRouteDesignators(conn, fare_route_id)
        elif fare_route:
            n, fare_route_ids = ReadFareRouteIds(conn, flight_number)
            for fare_route_id in fare_route_ids:
                m, fare_ids = ReadFareRoutes(conn, fare_route_id)
                for fare_id in fare_ids:
                    ReadFareAgencies(conn, fare_id)
        elif release_seat and dt1 is not None:
            if len(seat_numbers) == 0:
                print("No seat numbers supplied for seat release")
                conn.close()
                return 1
            if book_no is None:
                if locator is None:
                    print("No book number or locator")
                    return 1
                book_no = ReadLocator(conn, locator)
            n, origin_airport, destination_airport, departure_time = \
                ReadFlightDateLegInfo(conn, flight_number, dt1)
            if n == 0:
                print("Flight not found")
                conn.close()
                return 1
            flight = FlightData('Y', flight_number, dt1,
                                departure_time, arrival_time,
                                origin_airport, destination_airport, 0, company_code,
                                aircraft_code)
            CheckReleaseSeats(conn, book_no, flight, seat_numbers)
            FlightSeatBookings(conn, flight_number, dt1, origin_airport,
                               destination_airport)
        elif reserve_seat and dt1 is not None:
            if len(seat_numbers) == 0:
                print("No seat numbers supplied for seat reserve")
                conn.close()
                return 1
            n, origin_airport, destination_airport, departure_time = \
                ReadFlightDateLegInfo(conn, flight_number, dt1)
            if n == 0:
                print("Flight not found")
                return 1
            if book_no is None:
                if locator is None:
                    print("No book number or locator")
                    conn.close()
                    return 1
            flight = FlightData('Y', flight_number, dt1,
                                departure_time, arrival_time,
                                origin_airport, destination_airport,
                                0, company_code, aircraft_code)
            CheckReserveSeats(conn, book_no, flight, seat_numbers, 'Y')
        elif seat_all and dt1 is not None:
            n, origin_airport, destination_airport, departure_time = \
                ReadFlightDateLegInfo(conn, flight_number, dt1)
            if n == 0:
                print("Flight not found")
                conn.close()
                return 1
            flight = FlightData('Y', flight_number, dt1,
                                departure_time, arrival_time,
                                origin_airport, destination_airport,
                                0, company_code, aircraft_code)
            ReadFlightDateAllSeats(conn, flight)
        elif et_asr and dt1 is not None:
            if len(seat_numbers) == 0:
                print("No seat numbers supplied for seat end transaction check")
                conn.close()
                return 1
            if book_no is None:
                if locator is None:
                    print("No book number or locator")
                    conn.close()
                    return 1
                book_no = ReadLocator(conn, locator)
            flight = read_flight_data(conn, flight_number, dt1)
            for seat_number in seat_numbers:
                print("________________________")
                CheckSeatReservationEtAsr(conn, flight, seat_number, book_no)
        elif seat_book and dt1 is not None:
            ShowFlightSeats(conn, flight_number, dt1)
        elif release_seat and dt1 is not None:
            n, origin_airport, destination_airport, departure_time = \
                ReadFlightDateLegInfo(conn, flight_number, dt1)
            if n == 0:
                print("Flight not found")
                conn.close()
                return 1
            flight = FlightData('Y', flight_number, dt1,
                                departure_time, arrival_time,
                                origin_airport, destination_airport, 0, company_code,
                                aircraft_code)
            if locator is not None:
                book_no = ReadLocator(conn, locator)
            if book_no is None and len(seat_numbers) == 0:
                ReadReleaseSeats(conn, flight)
            elif book_no is None:
                print("No book number or locator supplied for seat release")
                conn.close()
                return 1
            elif len(seat_numbers) == 0:
                print("No seat numbers supplied for seat release")
                conn.close()
                return 1
            else:
                flight_seat_reservation_group_id, boarding_control_number_id = \
                    CheckReleaseSeats(conn, book_no, flight, seat_numbers)
                ReleaseSeat(conn, flight_seat_reservation_group_id,
                            boarding_control_number_id, update_db)
        elif chkit and desc_map and dt1 is not None:
            n, origin_airport, destination_airport, departure_time = \
                ReadFlightDateLegInfo(conn, flight_number, dt1)
            if n > 0:
                flight = FlightData('Y', flight_number, dt1,
                                    departure_time, arrival_time,
                                    origin_airport, destination_airport, 0,
                                    company_code, aircraft_code)
                CheckFlightDateClassSeatMaps(conn, flight)
        elif desc_map and dt1 is not None:
            n, origin_airport, destination_airport, departure_time = \
                ReadFlightDateLegInfo(conn, flight_number, dt1)
            if n > 0:
                flight = FlightData('Y', flight_number, dt1,
                                    departure_time, arrival_time,
                                    origin_airport, destination_airport, 0,
                                    company_code, aircraft_code)
                ReadFlightDateClassSeatMaps(conn, flight)
        #elif csflag and dt1 is not None:
            #if dt2 is not None:
                #for single_date in daterange(dt1, dt2):
                    #read_code_share(conn, flight_number, single_date, selling_class_code,
                                    #departure_airport, arrival_airport, int(city_pair))
            #else:
                #read_code_share(conn, flight_number, dt1, selling_class_code,
                                #departure_airport, arrival_airport, int(city_pair))
        elif dt1 is not None and len(seat_numbers) != 0:
            n, origin_airport, destination_airport, departure_time = \
                ReadFlightDateLegInfo(conn, flight_number, dt1)
            if n > 0:
                ReadReserveSeats(conn, flight_number, dt1, origin_airport,
                                 destination_airport, seat_numbers)
        elif dt1 is not None and recCount != 0:
            ReadFlightSegmDate(conn, flight_number, dt1, recCount,
                               reconcile_window)
        elif schedule_period_no > 0:
            ReadFlightPeriodsGui(conn, flight_number, schedule_period_no)
        elif test_periods:
            ReadTestPeriods(conn, flight_number)
        elif asm_ssm:
            if aircraft_code is None:
                print("No value for aircraft code")
                conn.close()
                return 1
            if dt1 is None or dt2 is None:
                print("No value for start and/or end dates")
                conn.close()
                return 1
            if frequency_code is None:
                print("No value for frequency code")
                conn.close()
                return 1
            ConfigTableNo, NoOfSeats = ReadConfigNumberOfSeats(conn,
                                                               aircraft_code)
            viaCities = "%3s#%3s" % (departure_airport, arrival_airport)
            ReadSchedPeriod(conn, dt1, dt2, frequency_code,
                            flight_number, frequency_code, viaCities, ConfigTableNo)
            n = GetFlightDataSsm(conn, flight_number, dt1, dt2, frequency_code)
            if n == 0:
                CheckSsmTim(conn, flight, dt1, dt2, frequency_code, aircraft_code)
        elif dt1 is not None:
            read_flight_stuff(conn, flight_number, dt1, selling_cls, None)
        else:
            ReadFlightPeriods(conn, flight_number)

    # Commit transaction and close connection
    conn.commit()
    conn.close()

    return rval


# Entry point
if __name__ == "__main__":
    rv = main(sys.argv[1:])
    try:
        sys.stdout.close()
    except:
        pass
    try:
        sys.stderr.close()
    except:
        pass
    sys.exit(rv)
