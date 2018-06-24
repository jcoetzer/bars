#!/usr/bin/python3
"""
Generate passenger name list.

@file PnlGen.py
"""

import os
import sys
import getopt

from PnlAdl.PaxList import PaxList
from ReadDateTime import ReadDate
from BarsLog import set_verbose, printlog
from BarsConfig import BarsConfig
from DbConnect import OpenDb, CloseDb
from PnlAdl.ReadPnl import PrintPnl


def usage(pname='PnlGen.py'):
    """Help message."""
    print("Usage: %s [-a|-p] [F <FLIGHT_NUMBER>] [-D <BOARD_DATE>]"
          " [-A <AIRPORT>]"
          % pname)
    print("\t-a       : ADL format")
    print("\t-p       : PNL format")
    sys.exit(1)


def main(argv):
    """Entry point."""
    rv = 0
    showPnl = True
    flightNumber = ''
    boardDate = None
    departAirport = ''

    barsdir = os.environ['BARSDIR']
    if barsdir is None:
        barsdir = "/opt/bars"
    etcdir = "%s/etc" % barsdir

    if len(argv) < 1:
        usage()

    try:
        opts, args = getopt.getopt(argv,
                                   "ahvVD:F:P:",
                                   ["help"])
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
        elif opt == "-a":
            showPnl = False
        elif opt == "-D":
            boardDate = ReadDate(arg)
            printlog(2, "Board date set to %s" % boardDate)
        elif opt == "-F":
            flightNumber = arg
            printlog(2, "Flight number set to %s" % flightNumber)
        elif opt == "-P":
            departAirport = arg
            printlog(2, "Departure airport set to %s" % departAirport)
        else:
            print("Unknown input '%s'" % arg)
            usage()

    cfg = BarsConfig('%s/bars.cfg' % etcdir)

    # Open connection to database
    conn = OpenDb(cfg.dbname, cfg.dbuser, cfg.dbhost)

    if flightNumber == '':
        print("No value for flight number")
        usage()

    if boardDate is None:
        print("No value for board date\n")
        usage()

    # Read current passengers
    paxData = PaxList(conn, flightNumber, boardDate)

    # Process input file
    rv = paxData.ReadDb(flightNumber, boardDate, departAirport)

    PrintPnl(paxData)

    # Commit transaction and close connection
    CloseDb(conn)

    return rv


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
