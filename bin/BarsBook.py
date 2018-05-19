#!/usr/bin/python
#
# BarsBook.py
#
"""Main for booking."""

import os
import sys
import getopt

import psycopg2

from BarsLog import printlog, set_verbose
from ReadDateTime import ReadDate

from SsmDb import GetCityPair
from AvailDb import get_selling_conf, get_avail_flights
from FlightDetails import GetFlightDetails
from FareCalcDisplay import FareCalcDisplay
from BookingInfo import AddBook, int2base20, AddItenary, AddPassenger, \
     AddBookFares, AddBookFareSegments, AddBookFarePassengers, \
     AddBookFaresPayments, AddBookRequest, AddPayment


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
    sys.exit(1)


def doPay(conn, aCurrency, aPayAmount, aBookNo, aPaxName, aPaxCode,
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
    bookno = 0

    vSeatQuantity = 1
    vOriginAddress = 'HDQOTJE'
    vOriginBranchCode = 'SNAFU'
    vAgencvCode = 'TARFU'
    vUser = 'JOHN'
    vGroup = 'BANANA'
    sellClass = 'Y'
    vFareNo = 1
    vPaxCode = 'ADULT'
    vCurrency = 'ZAR'
    vFareCode = 'XJEOW'
    vSource = 0

    if len(argv) < 1:
        usage(os.path.basename(sys.argv[0]))

    opts, args = getopt.getopt(argv,
                               "cfhivyVA:B:C:D:E:F:I:K:L:M:N:P:Q:R:S:T:X:Y:",
                               ["help",
                                "avail", "book", "detail", "price", "pay"
                                "bn=",
                                "dob="
                                "date=", "edate=", "flight="])

    dt1 = None
    dt2 = None
    arriveAirport = None
    departAirport = None
    doavail = False
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
    paxDob = None
    payAmount = None

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
        elif opt == '--detail':
            dodetail = True
        elif opt == '--price':
            doprice = True
        elif opt == '--pay':
            dopay = True
        elif opt == '--bn':
            bn = int(arg)
        elif opt in ("-A", "--amount"):
            payAmount = float(arg)
        elif opt == "--dob":
            bookno = int(arg)
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
        elif opt == "--dob":
            paxDob = str(arg).upper().split(',')
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
        return 0

    if dt1 is None:
        print("No departure date specified")
        return 1

    if dt2 is None:
        dt2 = dt1

    # Open connection to database
    try:
        connstr = "dbname='%s' user='%s' host='%s'" \
            % (dbname, 'postgres', 'localhost')
        conn = psycopg2.connect(connstr)
    except:
        print("Could not connect to database %s" % (dbname))
        return 1
    printlog(1, "Connected to database %s" % dbname)

    selling_cls_codes = get_selling_conf(conn, vCompany)
    cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
    if doavail:
        for selling_cls_code in selling_cls_codes:
            flights = get_avail_flights(conn, dt1, dt2, cityPairNo,
                                        departAirport, arriveAirport,
                                        selling_cls_code[0], vCompany)
            for flight in flights:
                flight.display()
    elif dodetail:
        GetFlightDetails(conn, flightNumber, dt1,
                         departAirport, arriveAirport)
    elif doprice:
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
    elif dobook:
        if payAmount is None:
            payAmount = 0.0
        vSeatQuantity = len(paxNames)
        bn = AddBook(conn, vSeatQuantity, vOriginAddress, vOriginBranchCode, vAgencvCode,
                     dt1.strftime('%Y-%m-%d'), vUser, vGroup)
        AddItenary(conn, bn, flightNumber, dt1,
                   departAirport, arriveAirport,
                   departTime, arriveTime,
                   departTerm, arriveTerm,
                   cityPairNo, sellClass,
                   vUser, vGroup)
        AddPassenger(conn, bn, 1,
                     paxNames,
                     'ADULT', 'A',
                     vUser, vGroup)
        AddBookFares(conn, bn, vFareNo, vPaxCode, departAirport, arriveAirport,
                     vCurrency,
                     payAmount, vUser, vGroup)
        AddBookFareSegments(conn, bn, vFareNo, vPaxCode, flightNumber, dt1,
                            departAirport, arriveAirport,
                            vCurrency, payAmount,
                            vUser, vGroup)
        AddBookFarePassengers(conn, bn, vPaxCode, vCurrency, payAmount,
                              vUser, vGroup)
        AddBookFaresPayments(conn, bn, vFareNo, vPaxCode, vFareCode,
                             vCurrency, payAmount, vUser, vGroup, vSource)
        AddBookRequest(conn, bn, vCompany, 'CKIN', paxDobs, vUser, vGroup)
    elif dopay:
        if bookno is None:
            print "Book number not specified"
            return 1
        vPaymentForm = 'VI'
        vPaymentType = 'CC'
        vDocNum = '4242424242424242'
        vPaymentMode = ' '
        vRemark = ' '
        AddPayment(conn, vPaymentForm, vPaymentType, vCurrency, payAmount,
                   vDocNum, vPaymentMode,
                   bookno, paxNames[0], vPaxCode,
                   vOriginBranchCode, vRemark,
                   vUser, vGroup)

    conn.commit()
    conn.close()
    printlog(1, "Disconnected")

    return 0


if __name__ == "__main__":
    """Entry point."""
    rv = main(sys.argv[1:])
    sys.exit(rv)
