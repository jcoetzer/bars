#!/usr/bin/python2
#
# AvailService.py
#
"""
Provide flight details.
"""

import os
import sys
import getopt
import logging
import psycopg2
from psycopg2 import extras

from BarsLog import blogger, init_blogger
from ReadDateTime import ReadDate, DateRange

from Ssm.SsmDb import GetCityPair
from Flight.FlightDetails import GetFlightDetails
from DbConnect import OpenDb, CloseDb
from BarsConfig import BarsConfig


def usage():
    print("Help!")
    sys.exit(1)


# Pythonic entry point
def main(argv):

    barsdir = os.environ['BARSDIR']
    etcdir = "%s/etc" % barsdir
    fname = None
    rv = 0

    if len(argv) < 1:
        usage()

    init_blogger("bars")
    opts, args = getopt.getopt(argv,
                               "cfhivyVA:B:C:D:E:F:I:K:L:M:N:P:Q:R:S:T:X:Y:",
                               ["help", "date=", "edate=", "flight="])

    dt1 = None
    dt2 = None
    arrive_airport = None
    depart_airport = None

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            usage()
        elif opt == '-v':
            _levelsetLevel(logging.INFO)
        elif opt == '-V':
            _levelsetLevel(logging.DEBUG)
        # elif opt in ("-C", "--class"):
            # selling_cls = str(arg).upper()
        elif opt in ("-D", "--date"):
            dt1 = ReadDate(arg)
            blogger().info("\t flight date %s" % dt1.strftime("%Y-%m-%d"))
        # elif opt in ("-E", "--edate"):
            # dt2 = ReadDate(arg)
        elif opt in ("-F", "--flight"):
            if ',' in arg:
                fndata = arg.split('/')
                flight_number = fndata[0]
                dt1 = ReadDate(fndata[1])
            else:
                flight_number = arg
            blogger().debug("Flight number set to %s" % flight_number)
        # elif opt in ("-P", "--depart"):
            # depart_airport = str(arg).upper()
            # blogger().info("\t depart %s" % depart_airport)
        # elif opt in ("-Q", "--arrive"):
            # arrive_airport = str(arg).upper()
            # blogger().info("\t arrive %s" % arrive_airport)
        else:
            pass

    if dt1 is None:
        print("No departure date specified")
        return 1

    if dt2 is None:
        dt2 = dt1

    cfg = BarsConfig('%s/bars.cfg' % etcdir)

    # Open connection to database
    conn = OpenDb(cfg.dbname, cfg.dbuser, cfg.dbhost)

    GetFlightDetails(conn, flight_number, dt1, depart_airport, arrive_airport)

    conn.commit()
    conn.close()
    blogger().info("Disconnected")

    return 0


# Entry point
if __name__ == "__main__":
    rv = main(sys.argv[1:])
    sys.exit(rv)
