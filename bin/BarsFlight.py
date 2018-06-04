#!/usr/bin/python

import os
import sys
import getopt
from configobj import ConfigObj
from xml.dom import minidom
import psycopg2
from datetime import datetime, timedelta, datetime
from ReadDateTime import ReadDate
from BarsLog import set_verbose, printlog
from Ssm.SsmDb import CheckCityPair, GetCityPair
from BarsConfig import BarsConfig
from DbConnect import OpenDb, CloseDb
from Flight.WriteFares import AddCityPair, AddFareSegments, AddFares
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


def usage(pname='BarsFlight.py'):
    print("Add city pair:\n\t%s --city -P <CITY> -Q<CITY>")
    print("Add fare:\n\t%s --fare -P <CITY> -Q<CITY> -R <AMOUNT> -D <DATE> -E <DATE>")
    sys.exit(2)


def main(argv):
    """Pythonic entry point."""
    barsdir = os.environ['BARSDIR']
    if barsdir is None:
        barsdir = "/opt/bars"
    etcdir = "%s/etc" % barsdir
    docity = False
    dofare = False
    dt1 = None
    dt2 = None
    payAmount = None
    departure_airport = None
    arrival_airport = None

    if len(argv) < 1:
        usage()

    try:
        opts, args = getopt.getopt(argv,
                                   "cfhivxyVA:B:C:D:E:F:I:K:L:M:N:P:Q:R:S:T:X:Y:",
                                   ["help", "city", "fare", "date=", "edate=", "flight=",
                                    "period=", "seats=", "days=", "class=",
                                    "locator=", "bookno=", "depart=", "arrive=",
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
        elif opt in ("-D", "--date"):
            dt1 = ReadDate(arg)
            printlog(1, "\t start date %s" % dt1.strftime("%Y-%m-%d"))
        elif opt in ("-E", "--edate"):
            dt2 = ReadDate(arg)
            printlog(1, "\t end date %s" % dt1.strftime("%Y-%m-%d"))
        elif opt in ("-P", "--depart"):
            departure_airport = str(arg).upper()
            printlog(1, "\t depart %s" % departure_airport)
        elif opt in ("-Q", "--arrive"):
            arrival_airport = str(arg).upper()
            printlog(1, "\t arrive %s" % arrival_airport)
        elif opt in ("-R", "--amount"):
            payAmount = int(arg)
        else:
            print("Unknown option '%s'" % opt)
            return 1

    files = []
    for arg in args:
        files.append(arg.strip())

    cfg = BarsConfig('%s/bars.cfg' % etcdir)

    # Open connection to database
    conn = OpenDb(cfg.dbname, cfg.dbuser, cfg.dbhost)

    if docity and departure_airport is not None and arrival_airport is not None:
        NewCityPair(conn, departure_airport, arrival_airport,
                    cfg.User, cfg.Group)
    elif docity:
        ReadCityPairs(conn)
    elif dofare and departure_airport is not None \
    and arrival_airport is not None and dt1 is not None and dt2 is not None:
        city_pair = GetCityPair(conn, departure_airport, arrival_airport)
        if city_pair > 0:
            AddFareSegments(conn, cfg.CompanyCode,
                            departure_airport, arrival_airport, city_pair,
                            dt1, dt2, payAmount,
                            cfg.User, cfg.Group)
            AddFares(conn, cfg.CompanyCode, departure_airport, arrival_airport,
                     cfg.SellingClasses, cfg.User, cfg.Group)
    elif dofare:
        ReadFareCodes(conn)
        ReadFareSegments(conn)
    else:
        print "Huh?"

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
