#!/usr/bin/python
#
# BarsBook.py
#
"""Main for booking."""

import os
import sys
import getopt
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

import psycopg2

from BarsLog import printlog, set_verbose
from ReadDateTime import ReadDate

from SsmDb import GetCityPair
from AvailDb import get_selling_conf, get_avail_flights
from FlightDetails import GetFlightDetails
from FareCalcDisplay import FareCalcDisplay
from BookingInfo import AddBookCrossIndex, AddBook, int2base20, AddItenary, AddPassenger, \
     AddBookFares, AddBookFareSegments, AddBookFarePassengers, \
     AddBookFaresPayments, AddBookRequest, AddPayment, \
     GetPreBookingInfo, AddBookTimeLimit


def usage(pn):
    """Help message."""
    print("Availability:")
    print("\t%s --avail -P <CITY> -Q <CITY> -D <DATE> [-E <DATE>]" % pn)
    print("Pricing:")
    print("\t%s --price -C <CLASS> -P <CITY> -Q <CITY> -D <DATE> [-E <DATE>]" % pn)
    print("Detail:")
    print("\t%s --detail -F <FLIGHT> -P <CITY> -Q <CITY> -D <DATE> [-E <DATE>]" % pn)
    print("Book:")
    print("\t%s --book -N <PAX> -F <FLIGHT> -P <CITY> -Q <CITY> -D <DATE> [-E <DATE>]" % pn)
    print("Check:")
    print("\t%s --chk -B <BOOK>" % pn)
    sys.exit(1)


def OpenDb(dbname):
    """Open connection to database."""
    try:
        connstr = "dbname='%s' user='%s' host='%s'" \
            % (dbname, 'postgres', 'localhost')
        conn = psycopg2.connect(connstr)
    except:
        print("Could not connect to database %s" % (dbname))
        return 1
    printlog(1, "Connected to database %s" % dbname)
    return conn


def CloseDb(conn):
    """Close connection to database."""
    conn.commit()
    conn.close()
    printlog(1, "Disconnected")


def GetAvail(conn, dt1, dt2, cityPairNo,
             departAirport, arriveAirport,
             selling_cls_codes, vCompany):
    """Get availability information."""
    for selling_cls_code in selling_cls_codes:
        flights = get_avail_flights(conn, dt1, dt2, cityPairNo,
                                    departAirport, arriveAirport,
                                    selling_cls_code[0], vCompany)
        for flight in flights:
            flight.display()


def GetPrice(conn,
             vCompany,
             cityPairNo,
             dt1,
             dt2,
             selling_cls_code,
             onw_return_ind,
             fare_category,
             authority_level):
    """Get price information."""
    fares = FareCalcDisplay(conn,
                            vCompany,
                            cityPairNo,
                            dt1.strftime('%Y-%m-%d'),
                            dt2.strftime('%Y-%m-%d'),
                            selling_cls_code,
                            onw_return_ind,
                            fare_category,
                            authority_level,
                            dt2.strftime('%Y-%m-%d'))
    for fare in fares:
        fare.display()


def GetBook(conn, vCompany, vBookCategory, vOriginAddress,
            vOriginBranchCode, vAgencyCode,
            paxNames, paxDobs,
            payAmount,
            flightNumber, dt1,
            departAirport, arriveAirport,
            departTime, arriveTime,
            departTerm, arriveTerm,
            cityPairNo, sellClass,
            aTimeLimit,
            vUser, vGroup):
    """Make a booking."""
    if payAmount is None:
        payAmount = 0.0
    vSeatQuantity = len(paxNames)
    bn, pnr = AddBookCrossIndex(conn, vBookCategory, vOriginAddress,
                                vUser, vGroup)
    AddBook(conn, bn, pnr, vSeatQuantity, vBookCategory,
            vOriginAddress, vOriginBranchCode, vAgencyCode,
            dt1.strftime('%Y-%m-%d'), vUser, vGroup)
    AddItenary(conn, bn, flightNumber, dt1,
               departAirport, arriveAirport,
               departTime, arriveTime,
               departTerm, arriveTerm,
               cityPairNo, sellClass,
               vUser, vGroup)
    AddPassenger(conn, bn,
                 paxNames,
                 'ADULT', 'A',
                 vUser, vGroup)
    AddBookRequest(conn, bn, vCompany, 'CKIN', paxDobs, vUser, vGroup)
    AddBookTimeLimit(conn, bn, vAgencyCode, vUser, vGroup)


def GetPay(conn, aCurrency, aPayAmount, aBookNo, aPaxName, aPaxCode,
           aOriginBranchCode,
           aUser, aGroup):
    """Process payment."""
    if aBookNo is None:
        print "Book number not specified"
        return 1
    vPaymentForm = 'VI'
    vPaymentType = 'CC'
    vDocNum = '4242424242424242'
    vPaymentMode = ' '
    vRemark = ' '
    AddPayment(conn, vPaymentForm, vPaymentType, aCurrency, aPayAmount,
               vDocNum, vPaymentMode,
               aBookNo, aPaxName, aPaxCode,
               aOriginBranchCode, vRemark,
               aUser, aGroup)
    return 0


# TODO Cyclomatic complexity too high
def main(argv):
    """Pythonic entry point."""
    global verbose

    dbname = 'barsdb'
    onw_return_ind = 'R'
    authority_level = 100
    fare_category = 'JEOW'
    vCompany = 'JE'
    selling_cls_code = 'Y'

    vOriginAddress = 'HDQOTJE'
    vOriginBranchCode = 'SNAFU'
    vAgencyCode = 'TARFU'
    vUser = 'JOHN'
    vGroup = 'BANANA'
    sellClass = 'Y'
    vPaxCode = 'ADULT'
    vCurrency = 'ZAR'
    vFareCode = 'XJEOW'
    vBookCategory = 'S'     # or G for groups

    if len(argv) < 1:
        usage(os.path.basename(sys.argv[0]))

    opts, args = getopt.getopt(argv,
                               "cfhivyVA:B:C:D:E:F:I:K:L:M:N:P:Q:R:S:T:X:Y:",
                               ["help",
                                "avail", "book", "detail", "price", "pay", "chk",
                                "bn=",
                                "dob="
                                "date=", "edate=", "flight="])

    dt1 = None
    dt2 = None
    arriveAirport = None
    departAirport = None
    doavail = False
    dochk = False
    dodetail = False
    doprice = False
    dobook = False
    dopay = False
    departTerm = 'A'
    arriveTerm = 'B'
    bn = None
    departTime = None
    arriveTime = None
    paxNames = None
    paxDobs = None
    payAmount = None
    vTimeLimit = datetime.now() + timedelta(days=2)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            usage(os.path.basename(sys.argv[0]))
        elif opt == '-v':
            set_verbose(1)
        elif opt == '-V':
            set_verbose(2)
        elif opt == '--avail':
            doavail = True
        elif opt == '--book':
            dobook = True
        elif opt == '--chk':
            printlog(2, "Check booking")
            dochk = True
        elif opt == '--detail':
            dodetail = True
        elif opt == '--price':
            doprice = True
        elif opt == '--pay':
            dopay = True
        elif opt in ("-A", "--amount"):
            payAmount = float(arg)
        elif opt in ('-B', '--bn'):
            bn = int(arg)
            printlog(2, "Booking number %d" % bn)
        elif opt in ("-C", "--class"):
            selling_cls_code = str(arg).upper()
        elif opt in ("-D", "--date"):
            dt1 = ReadDate(arg)
            printlog(1, "\t flight date %s" % dt1.strftime("%Y-%m-%d"))
        elif opt in ("-E", "--edate"):
            dt2 = ReadDate(arg)
        elif opt in ("-F", "--flight"):
            if ',' in arg:
                fndata = arg.split('/')
                flightNumber = fndata[0]
                dt1 = ReadDate(fndata[1])
            else:
                flightNumber = arg
            printlog(2, "Flight number set to %s" % flightNumber)
        elif opt in ("-N", "--name"):
            paxNames = str(arg).upper().split(',')
        elif opt in ("-M", "--dob"):
            paxDobs = str(arg).upper().split(',')
        elif opt in ("-P", "--depart"):
            departAirport = str(arg).upper()
            printlog(1, "\t depart %s" % departAirport)
        elif opt in ("-Q", "--arrive"):
            arriveAirport = str(arg).upper()
            printlog(1, "\t arrive %s" % arriveAirport)
        elif opt == "-X":
            departTime = arg
        elif opt == "-Y":
            arriveTime = arg
        else:
            pass

    if bn is not None:
        pnr = int2base20(bn)
        print("Booking %d PNR %s" % (bn, pnr))

    # Open connection to database
    conn = OpenDb(dbname)

    if dochk:
        print("Check booking %d" % bn)
        GetPreBookingInfo(conn, bn)
        return 0

    if dt1 is None:
        print("No departure date specified")
        return 1

    if dt2 is None:
        dt2 = dt1

    selling_cls_codes = get_selling_conf(conn, vCompany)
    cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
    if doavail:
        GetAvail(conn, dt1, dt2, cityPairNo,
                 departAirport, arriveAirport,
                 selling_cls_codes, vCompany)
    elif dodetail:
        GetFlightDetails(conn, flightNumber, dt1,
                         departAirport, arriveAirport)
    elif doprice:
        GetPrice(conn,
                 vCompany,
                 cityPairNo,
                 dt1,
                 dt2,
                 selling_cls_code,
                 onw_return_ind,
                 fare_category,
                 authority_level)
    elif dobook:
        GetBook(conn, vCompany, vBookCategory, vOriginAddress,
                vOriginBranchCode, vAgencyCode,
                paxNames, paxDobs,
                payAmount,
                flightNumber, dt1,
                departAirport, arriveAirport,
                departTime, arriveTime,
                departTerm, arriveTerm,
                cityPairNo, sellClass,
                vTimeLimit,
                vUser, vGroup)
    elif dopay:
        GetPay(conn, vCurrency, payAmount, bn, paxNames, vPaxCode,
               vOriginBranchCode,
               vUser, vGroup)
    else:
        print("Nothing to do")

    CloseDb(conn)

    return 0


if __name__ == "__main__":
    """Entry point."""
    rv = main(sys.argv[1:])
    sys.exit(rv)
