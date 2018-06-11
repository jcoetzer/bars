#!/usr/bin/python3
#
# BarsBook.py
#
"""
Main for booking.
"""

import os
import sys
import getopt
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
from random import randrange
import configparser
from faker import Faker
from random import randint

from BarsLog import printlog, set_verbose
from ReadDateTime import ReadDate

from Ssm.SsmDb import GetCityPair
from Flight.AvailDb import get_selling_conf, get_avail_flights, OldAvailSvc
from Flight.FlightDetails import GetFlightDetails
from Booking.FareCalcDisplay import FareCalcDisplay
from Booking.BookingInfo import AddBookCrossIndex, AddBook, int2base20, \
     AddItenary, AddPassenger, \
     AddBookFares, AddBookFareSegments, AddBookFarePassengers, \
     AddBookFaresPayments, AddBookRequest, AddPayment, \
     GetPreBookingInfo, AddBookTimeLimit, AddContact
from Booking.ReadItenary import ReadItenary
from Flight.ReadFlights import ReadDeparture
from Flight.ReadFlights import ReadFlightDeparture
from DbConnect import OpenDb, CloseDb
from BarsConfig import BarsConfig
from BarsBanner import print_banner
from Booking.ReadBooking import ReadPassengers
from Booking.PassengerData import PassengerData


def usage(pn):
    """Help message."""
    print_banner()
    print("Availability:")
    print("\t%s --avail -P <CITY> -Q <CITY> -D <DATE> [-E <DATE>]" % pn)
    print("Pricing:")
    print("\t%s --price -C <CLASS> -P <CITY> -Q <CITY> -D <DATE> [-E <DATE>]"
          % pn)
    print("Detail:")
    print("\t%s --detail -F <FLIGHT> -P <CITY> -Q <CITY> -D <DATE> [-E <DATE>]"
          % pn)
    print("Book:")
    print("\t%s --book -N <PAX> -F <FLIGHT> -N <NAME> -M <MISC> -D <DATE>"
          " [-E <DATE>]" % pn)
    print("Check:")
    print("\t%s --pay -B <BOOK> -A <AMOUNT> -N <NAME>" % pn)
    print("Check:")
    print("\t%s --chk -B <BOOK>" % pn)
    sys.exit(1)


def random_date(start, end):
    """
    Generate random datetime between two datetimes.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def GetAvail(conn, dt1, dt2, cityPairNo,
             departAirport, arriveAirport,
             selling_classes, vCompany):
    """Get availability information."""
    flights = OldAvailSvc(conn, vCompany, dt1, cityPairNo,
                          departAirport, arriveAirport)
    for flight in flights:
        flight.display()
    for selling_class in selling_classes:
        flights = get_avail_flights(conn, dt1, dt2, cityPairNo,
                                    departAirport, arriveAirport,
                                    selling_class[0], vCompany)
        for flight in flights:
            flight.display()


def GetPrice(conn,
             vCompany,
             cityPairNo,
             dt1,
             dt2,
             selling_class,
             onw_return_ind,
             fare_category,
             authority_level):
    """Get price information."""
    fares = FareCalcDisplay(conn,
                            vCompany,
                            cityPairNo,
                            dt1.strftime('%Y-%m-%d'),
                            dt2.strftime('%Y-%m-%d'),
                            selling_class,
                            onw_return_ind,
                            fare_category,
                            authority_level,
                            dt2.strftime('%Y-%m-%d'))
    for fare in fares:
        fare.display()

def GetPassengers(conn, bn):
    """Read and display passengers in booking."""
    paxRecs = ReadPassengers(conn, bn)
    for paxRec in paxRecs:
        paxRec.display()
    return paxRecs


def GetItenary(conn, aBookNo):
    """Read and display itenaries for booking."""
    itenRecs = ReadItenary(conn, aBookNo, '', '')
    for itenRec in itenRecs:
        itenRec.display()
    return itenRecs


def PutBook(conn, vCompany, vBookCategory, vOriginAddress,
            vOriginBranchCode, vAgencyCode,
            paxRecs,
            payAmount,
            flightNumber, dt1,
            flightNumber2, dt2,
            departAirport, arriveAirport,
            sellClass,
            aTimeLimit,
            vUser, vGroup):
    """Make a booking."""
    if paxRecs is None:
        print("No passenger names")
        return
    vSeatQuantity = len(paxRecs)
    if payAmount is None:
        payAmount = 0.0
    if sellClass is None:
        sellClass = 'Y'
    #if departAirport is None or arriveAirport is None:
        #print("Flight number and date must be specified")
        #return
    n, fd = ReadFlightDeparture(conn, sellClass, flightNumber, dt1)
    if n == 0:
        print("Flight number and date not found")
        return
    departAirport = fd.departure_airport
    arriveAirport = fd.arrival_airport
    cityPairNo = fd.city_pair
    departTerm = fd.departure_terminal
    arriveTerm = fd.arrival_terminal
    departTime = fd.departure_time
    arriveTime = fd.arrival_time
    bn, pnr = AddBookCrossIndex(conn, vBookCategory, vOriginAddress,
                                vUser, vGroup)
    AddBook(conn, bn, pnr, vSeatQuantity, vOriginAddress, vBookCategory,
            vOriginBranchCode, vAgencyCode,
            dt1.strftime('%Y-%m-%d'), vUser, vGroup)
    AddItenary(conn, bn, flightNumber, dt1,
               departAirport, arriveAirport,
               departTime, arriveTime,
               departTerm, arriveTerm,
               cityPairNo, sellClass,
               vUser, vGroup)
    if flightNumber2 is not None and dt2 is not None:
        n, fd = ReadFlightDeparture(conn, sellClass, flightNumber2, dt2)
        if n == 0:
            print("Return flight number and date not found")
            return
        departAirport = fd.departure_airport
        arriveAirport = fd.arrival_airport
        cityPairNo = fd.city_pair
        departTerm = fd.departure_terminal
        arriveTerm = fd.arrival_terminal
        departTime = fd.departure_time
        arriveTime = fd.arrival_time
        AddItenary(conn, bn, flightNumber2, dt2,
                   departAirport, arriveAirport,
                   departTime, arriveTime,
                   departTerm, arriveTerm,
                   cityPairNo, sellClass,
                   vUser, vGroup)

    AddPassenger(conn, bn, paxRecs, vUser, vGroup)
    AddContact(conn, bn, paxRecs, vUser, vGroup)
    paxRequests = []
    for paxRec in paxRecs:
        paxRequests.append(paxRec.date_of_birth)
    AddBookRequest(conn, bn, vCompany, 'CKIN', paxRequests, vUser, vGroup)
    AddBookTimeLimit(conn, bn, vAgencyCode, vUser, vGroup)


def PutPay(conn, aBookNo, aSellClass,
           aCurrency, aPayAmount, aPayAmount2,
           aCompany, aOriginBranchCode, aFareCode,
           vPaymentType, vPaymentForm, vDocNum,
           aUser, aGroup):
    """Process payment."""
    if aBookNo is None:
        print("Book number not specified")
        return 1
    paxRecs = GetPassengers(conn, aBookNo)
    # itenRecs = GetItenary(conn, aBookNo)
    vPaymentMode = ' '
    vRemark = ' '
    vFareNo = 1
    AddPayment(conn, vPaymentForm, vPaymentType, aCurrency, int(aPayAmount),
               vDocNum, vPaymentMode,
               aBookNo, paxRecs[0].passenger_name, paxRecs[0].passenger_code,
               aOriginBranchCode, vRemark,
               aUser, aGroup)

    payAmounts = [int(aPayAmount*100), int(aPayAmount2*100)]
    irecs = ReadItenary(conn, aBookNo, None, None,
                        fnumber=None, start_date=None, end_date=None)
    if len(irecs) > 2:
        print("Found %d itenaries")
        return 1
    else:
        n = 0
        for irec in irecs:
            irec.display()
            AddBookFares(conn, aBookNo, vFareNo, paxRecs[0].passenger_code,
                         irec.departure_airport, irec.arrival_airport,
                         aCurrency, payAmounts[n], aUser, aGroup)
            AddBookFaresPayments(conn, aBookNo, vFareNo,
                                 paxRecs[0].passenger_code, aFareCode,
                                 aCurrency, payAmounts[n],
                                 aUser, aGroup)
            n += 1

    return 0


# TODO Cyclomatic complexity too high
def main(argv):
    """Pythonic entry point."""

    barsdir = os.environ['BARSDIR']
    etcdir = "%s/etc" % barsdir

    # Option values
    dt1 = None
    dt2 = None
    arriveAirport = None
    departAirport = None
    flightNumber = None
    flightNumber2 = None
    departTerm = 'A'
    arriveTerm = 'B'
    bn = None
    departTime = None
    arriveTime = None
    paxNames = []
    paxDobs = []
    payAmount = 0.0
    payAmount2 = 0.0
    sellClass = None
    vTimeLimit = datetime.now() + timedelta(days=2)
    vDocNum = None

    # Option flags
    doavail = False
    dochk = False
    dodetail = False
    doprice = False
    dobook = False
    dopay = False

    if len(argv) < 1:
        usage(os.path.basename(sys.argv[0]))

    opts, args = getopt.getopt(argv,
                               "cfhivyVB:C:D:E:F:G:I:K:L:M:N:P:Q:R:S:T:X:Y:",
                               ["help",
                                "avail", "book", "detail", "price", "pay",
                                "chk",
                                "bn=", "dob=", "card=",
                                "date=", "edate=", "flight=", "rflight="])

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
        elif opt in ("-R", "--amount"):
            payAmount = float(arg)
        elif opt in ("-S", "--ramount"):
            payAmount2 = float(arg)
        elif opt in ("-T", "--card"):
            vDocNum = str(arg)
        elif opt in ('-B', '--bn'):
            bn = int(arg)
            printlog(2, "Booking number %d" % bn)
        elif opt in ("-C", "--class"):
            selling_class = str(arg).upper()
        elif opt in ("-D", "--date"):
            dt1 = ReadDate(arg)
            printlog(1, "\t flight date %s" % dt1.strftime("%Y-%m-%d"))
        elif opt in ("-E", "--edate"):
            printlog(1, "\t end date %s" % dt1.strftime("%Y-%m-%d"))
            dt2 = ReadDate(arg)
        elif opt in ("-F", "--flight"):
            if ',' in arg:
                fndata = arg.split('/')
                flightNumber = fndata[0]
                dt1 = ReadDate(fndata[1])
            else:
                flightNumber = arg
            printlog(2, "Flight number set to %s" % flightNumber)
        elif opt in ("-G", "--rflight"):
            if ',' in arg:
                fndata = arg.split('/')
                flightNumber2 = fndata[0]
                dt2 = ReadDate(fndata[1])
            else:
                flightNumber2 = arg
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

    cfg = BarsConfig('%s/bars.cfg' % etcdir)

    # Open connection to database
    conn = OpenDb(cfg.dbname, cfg.dbuser, cfg.dbhost)

    if dochk:
        print("Check booking %d" % bn)
        GetPreBookingInfo(conn, bn)
        return 0

    if dt1 is None and bn is None:
        print("No departure date or booking number specified")
        return 1

    if dt2 is None:
        dt2 = dt1

    selling_classs = get_selling_conf(conn, cfg.CompanyCode)
    if doavail:
        cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
        GetAvail(conn, dt1, dt2, cityPairNo,
                 departAirport, arriveAirport,
                 selling_classs, cfg.CompanyCode)
    elif dodetail:
        GetFlightDetails(conn, flightNumber, dt1, departAirport, arriveAirport)
        if flightNumber2 is not None and dt2 is not None:
            GetFlightDetails(conn, flightNumber2, dt2, departAirport,
                             arriveAirport)
    elif doprice:
        cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
        GetPrice(conn,
                 cfg.CompanyCode,
                 cityPairNo,
                 dt1,
                 dt2,
                 cfg.SellingClass,
                 cfg.OnwReturnIndicator,
                 cfg.FareCategory,
                 cfg.AuthorityLevel)
        cityPairNo = GetCityPair(conn, arriveAirport, departAirport)
        GetPrice(conn,
                 cfg.CompanyCode,
                 cityPairNo,
                 dt1,
                 dt2,
                 cfg.SellingClass,
                 cfg.OnwReturnIndicator,
                 cfg.FareCategory,
                 cfg.AuthorityLevel)
    elif dobook:
        # cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
        paxRecs = []
        if len(paxNames) == 0:
            lnames = randint(1, 9)
            n = 0
            while n < lnames:
                paxRec = PassengerData('ADULT', n+1)
                paxRec.fakeit()
                paxRec.display()
                paxRecs.append(paxRec)
                n += 1
        else:
            n = 0
            for paxName in paxNames:
                paxRec = PassengerData('ADULT', n+1, paxName, paxDobs[n])
                paxRecs.append(paxRec)
                n += 1
        PutBook(conn, cfg.CompanyCode, cfg.BookCategory, cfg.OriginAddress,
                cfg.OriginBranchCode, cfg.AgencyCode,
                paxRecs,
                payAmount,
                flightNumber, dt1,
                departAirport, arriveAirport,
                departTime, arriveTime,
                sellClass,
                vTimeLimit,
                cfg.User, cfg.Group)
    elif dopay:
        if payAmount is None:
            print("Payment amount not specified")
        else:
            vPaymentForm = 'VI'
            vPaymentType = 'CC'
            if vDocNum is None:
                fake = Faker()
                vDocNum = fake.credit_card_number()
            PutPay(conn, bn, sellClass,
                   cfg.Currency, payAmount, payAmount2,
                   cfg.CompanyCode, cfg.OriginBranchCode, cfg.FareCode,
                   vPaymentType, vPaymentForm, vDocNum,
                   cfg.User, cfg.Group)
    elif bn is not None:
        GetPassengers(conn, bn)
        GetItenary(conn, bn)
    else:
        print("Nothing to do")

    CloseDb(conn)

    return 0


if __name__ == "__main__":
    """Entry point."""
    rv = main(sys.argv[1:])
    sys.exit(rv)
