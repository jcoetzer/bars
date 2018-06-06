#!/usr/bin/python

import os
import sys
import getopt
from configobj import ConfigObj
from xml.dom import minidom
import psycopg2
from datetime import datetime, timedelta, datetime
from ReadDateTime import ReadDate, ReadTime
from BarsLog import set_verbose, printlog
from Ssm.SsmDb import CheckCityPair, GetCityPair
from ScheduleData import SsmData
from Ssm.ProcNew import ProcNew
from BarsConfig import BarsConfig
from DbConnect import OpenDb, CloseDb
from Flight.WriteFares import AddCityPair, AddFareSegments, AddFares, \
    DelFareSegments
from Flight.ReadFares import ReadCityPairs, ReadFareSegments, ReadFareCodes


def NewCityPair(conn, departure_airport, arrival_airport, userName, groupName):
    """Process new flight."""
    city_pair_id = CheckCityPair(conn,
                                 departure_airport,
                                 arrival_airport,
                                 1,
                                 userName,
                                 groupName)
    if city_pair_id == 0:
        city_pair_id = AddCityPair(conn, departure_airport,
                                   arrival_airport,
                                   userName, groupName)
    return city_pair_id


def NewFlight(conn, aAddress, aSender, aTimeMode,
              aFlightNumber, aFlightDateStart, aFlightDateEnd,
              aDepartCity, aDepartTime, aArriveCity, aArriveTime,
              aAircraftCode, aFrequencyCode, aCodeshare, aTailNumber,
              aUserName, aGroupName):
    """Create new flight."""
    ssm = SsmData(aAddress, aSender, aTimeMode,
                  aFlightNumber, aFlightDateStart, aFlightDateEnd,
                  aDepartCity, aDepartTime, aArriveCity, aArriveTime,
                  aAircraftCode, aFrequencyCode, aCodeshare, aTailNumber)
    if not ssm.check():
        print("Data error")
        return
    ProcNew(conn, ssm, aUserName, aGroupName)


def usage(pname='BarsFlight.py'):
    """Help message."""
    print("Add city pair:\n\t%s --city -P <CITY> -Q<CITY>")
    print("Add fare:\n\t%s --fare -P <CITY> -Q<CITY> -R <AMOUNT>"
          "-D <DATE> -E <DATE>" % pname)
    print("Write flight data :")
    print("\t%s --cnl|--eqt|--new|--rpl|--tim" % pname)
    print("\t\t -F <FLIGHT> -D <DATE> -Q <FREQ>")
    print("\t\t [-E <DATE>] [-A <CODE>] [-I <TIME>] [-J <TIME>] [-K <CITY>]"
          "[-L <CITY>] [-G <FLIGHT>] [-T <TAIL>]")
    print("where")
    print("\t-v\t\t Additional output")
    print("\t--cnl\t\t Cancel flight")
    print("\t--eqt\t\t Equipment change")
    print("\t--new\t\t New flight")
    print("\t--rpl\t\t Replace flight")
    print("\t--tim\t\t Time change")
    print("\t--utc\t\t Time zone UTC (default is LT)")
    print("\t-A <CODE>\t Aircraft code, e.g. 738")
    print("\t-D <DATE>\t Start date, e.g. 11/06/2018")
    print("\t-E <DATE>\t End date, e.g. 11/26/2018")
    print("\t-F <FLIGHT>\t Flight number, e.g. ZZ123")
    print("\t-G <FLIGHT>\t Codeshare flight number, e.g YY2164")
    print("\t-K <FREQ>\t Frequency code for weekdays, e.g. 34 (Monday is 1)")
    print("\t-P <CITY>\t Departure airport, e.g. JNB")
    print("\t-Q <CITY>\t Arrival airport, e.g. CPT")
    print("\t-T <TAIL>\t Tail number, e.g. ZSBZZ")
    print("\t-X <TIME>\t Departure time, e.g. 1120")
    print("\t-Y <TIME>\t Arrival time, e.g. 1325")
    sys.exit(2)


def main(argv):
    """Pythonic entry point."""
    barsdir = os.environ['BARSDIR']
    if barsdir is None:
        barsdir = "/opt/bars"
    etcdir = "%s/etc" % barsdir
    docity = False
    dofare = False
    dofaredel = False
    donew = False
    dt1 = None
    dt2 = None
    payAmount = None
    departure_airport = None
    arrival_airport = None
    flightNumber = None
    departTime = None
    arriveTime = None
    aircraftCode = None
    frequencyCode = '1234567'

    if len(argv) < 1:
        usage()

    try:
        opts, args = getopt.getopt(argv,
                                   "cfhivxyVA:D:E:F:G:K:P:Q:R:T:X:Y:",
                                   ["help", "city", "fare", "faredel",
                                    "new", "eqt", "cnl", "tim", "rpl",
                                    "utc",
                                    "date=", "edate=", "flight=",
                                    "depart=", "arrive=",
                                    "share=",
                                    "aircraft=", "freq=", "cfgtable="
                                    ])
    except getopt.GetoptError:
        print("Error in options")
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            usage()
        elif opt == '-v':
            # Debug output
            set_verbose(1)
        elif opt == '-V':
            # Debug output
            set_verbose(2)
        elif opt == "--city":
            docity = True
        elif opt == "--fare":
            dofare = True
        elif opt == "--faredel":
            dofaredel = True
        elif opt == "--new":
            donew = True
        elif opt == "-A" or opt == "--aircraft":
            aircraftCode = str(arg).upper()
            printlog(1, "\t aircraft code %s" % aircraftCode)
        elif opt in ("-D", "--date"):
            dt1 = ReadDate(arg)
            printlog(1, "\t start date %s" % dt1.strftime("%Y-%m-%d"))
        elif opt in ("-E", "--edate"):
            dt2 = ReadDate(arg)
            printlog(1, "\t end date %s" % dt1.strftime("%Y-%m-%d"))
        elif opt in ("-F", "--flight"):
            flightNumber = arg
        elif opt in ("-G", "--share"):
            codeShare = arg
        elif opt in ("-K", "--freq"):
            frequencyCode = str(arg)
        elif opt in ("-P", "--depart"):
            departure_airport = str(arg).upper()
            printlog(1, "\t depart %s" % departure_airport)
        elif opt in ("-Q", "--arrive"):
            arrival_airport = str(arg).upper()
            printlog(1, "\t arrive %s" % arrival_airport)
        elif opt in ("-R", "--amount"):
            payAmount = int(arg)
        elif opt in ("-T", "--tail"):
            tailNumber = str(arg)
        elif opt == "-X":
            departTime = ReadTime(arg)
        elif opt == "-Y":
            arriveTime = ReadTime(arg)
        else:
            print("Unknown option '%s'" % opt)
            return 1

    files = []
    for arg in args:
        files.append(arg.strip())

    cfg = BarsConfig('%s/bars.cfg' % etcdir)

    # Open connection to database
    conn = OpenDb(cfg.dbname, cfg.dbuser, cfg.dbhost)

    if donew:
        NewFlight(conn, cfg.Address, cfg.Sender, cfg.TimeMode,
                  flightNumber, dt1, dt2,
                  departure_airport, departTime, arrival_airport, arriveTime,
                  aircraftCode, frequencyCode, codeShare, tailNumber,
                  cfg.User, cfg.Group)
    elif docity and departure_airport is not None \
            and arrival_airport is not None:
        NewCityPair(conn, departure_airport, arrival_airport,
                    cfg.User, cfg.Group)
    elif docity:
        ReadCityPairs(conn)
    elif dofare and departure_airport is not None \
            and arrival_airport is not None and dt1 is not None \
            and dt2 is not None:
        city_pair = GetCityPair(conn, departure_airport, arrival_airport)
        if city_pair > 0:
            AddFareSegments(conn, cfg.CompanyCode,
                            departure_airport, arrival_airport, city_pair,
                            dt1, dt2, payAmount,
                            cfg.User, cfg.Group)
            AddFares(conn, cfg.CompanyCode, departure_airport, arrival_airport,
                     cfg.SellingClasses, cfg.User, cfg.Group)
    elif dofaredel and departure_airport is not None \
            and arrival_airport is not None and dt1 is not None \
            and dt2 is not None:
        DelFareSegments(conn, cfg.CompanyCode,
                        departure_airport, arrival_airport, dt1, dt2)
    elif dofare:
        ReadFareCodes(conn)
        ReadFareSegments(conn)
    else:
        print("Huh?")

    # Commit transaction and close connection
    CloseDb(conn)

    return 0


if __name__ == "__main__":
    """Entry point."""
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
