#!/usr/bin/python
#
# AvailService.py
#


import sys
import getopt

import psycopg2

from BarsLog import printlog, set_verbose
from ReadDateTime import ReadDate, DateRange

from SsmDb import GetCityPair
from FlightDetails import GetFlightDetails
from DbConnect import OpenDb, CloseDb


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
            set_verbose(1)
        elif opt == '-V':
            set_verbose(2)
        # elif opt in ("-C", "--class"):
            # selling_cls = str(arg).upper()
        elif opt in ("-D", "--date"):
            dt1 = ReadDate(arg)
            printlog(1, "\t flight date %s" % dt1.strftime("%Y-%m-%d"))
        # elif opt in ("-E", "--edate"):
            # dt2 = ReadDate(arg)
        elif opt in ("-F", "--flight"):
            if ',' in arg:
                fndata = arg.split('/')
                flight_number = fndata[0]
                dt1 = ReadDate(fndata[1])
            else:
                flight_number = arg
            printlog(2, "Flight number set to %s" % flight_number)
        # elif opt in ("-P", "--depart"):
            # depart_airport = str(arg).upper()
            # printlog(1, "\t depart %s" % depart_airport)
        # elif opt in ("-Q", "--arrive"):
            # arrive_airport = str(arg).upper()
            # printlog(1, "\t arrive %s" % arrive_airport)
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
    printlog(1, "Disconnected")

    return 0


# Entry point
if __name__ == "__main__":
    rv = main(sys.argv[1:])
    sys.exit(rv)
