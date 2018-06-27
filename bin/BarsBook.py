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
from Booking.FareCalcDisplay import FareCalcDisplay, ReadPayments, \
     ReadSellingConfig, GetPriceSsr
from Booking.BookingInfo import AddBookCrossIndex, AddBook, int2base20, \
     AddItinerary, AddPassenger, \
     AddBookFares, AddBookFarePassengers, \
     AddBookFaresPayments, AddBookRequests, AddBookRequest, AddPayment, \
     GetPreBookingInfo, AddBookTimeLimit, AddContact, UpdateBookPayment, \
     AddBookingFareSegments
from Booking.ReadItinerary import ReadItinerary, UpdateItinerary, UpdateBook
from Flight.ReadFlights import ReadDeparture
from Flight.ReadFlights import ReadFlightDeparture
from DbConnect import OpenDb, CloseDb
from BarsConfig import BarsConfig
from BarsBanner import print_banner
from Booking.ReadBooking import ReadPassengers
from Booking.PassengerData import PassengerData
from Flight.ReadTaxes import ReadTaxes, ApplyTaxes


def usage(pn):
    """Help message."""
    print_banner()
    print("Availability:")
    print("\t%s --avail -P <CITY> -Q <CITY> -D <DATE>" % pn)
    print("Pricing:")
    print("\t%s --price -C <CLASS> -P <CITY> -Q <CITY> -D <DATE>"
          % pn)
    print("Detail:")
    print("\t%s --detail -F <FLIGHT> -P <CITY> -Q <CITY> -D <DATE>"
          % pn)
    print("Book:")
    print("\t%s --book -N <NAME> -M <DATES> -F <FLIGHT> -D <DATE>" % pn)
    print("\t%s --book -F <FLIGHT> -D <DATE> [-L <COUNT>] [-K <GROUP>]" % pn)
    print("Pay:")
    print("\t%s --pay -B <BOOK> -A <AMOUNT> -N <NAME>" % pn)
    print("Service request:")
    print("\t%s --ssr -B <BOOK> -L <NUM> -U <CODE>:<TEXT>" % pn)
    print("Check:")
    print("\t%s --chk -B <BOOK>" % pn)
    print("where:")
    print("\t-A <AMOUNT>\t Payment amount")
    print("\t-B <BOOK>\t Booking number")
    print("\t-C <CLASS>\t Booking class")
    print("\t-D <DATE>\t Flight date")
    print("\t-F <FLIGHT>\t Flight number")
    print("\t-K <GROUP>\t Group name")
    print("\t-L <COUNT>\t Number of passengers")
    print("\t-K <GROUP>\t Group name")
    print("\t-M <DATES>\t Birth dates, comma seperated")
    print("\t-N <NAME>\t Passenger names, comma seperated")
    print("\t")
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
             aCompanyCode,
             departAirport, arriveAirport,
             dt1, dt2,
             selling_class, onw_return_ind, fare_category, authority_level):
    """Read and display price information."""
    sellconfigs = ReadSellingConfig(conn, aCompanyCode)
    # for cls in sorted(sellconfigs, key=sellconfigs.get, reverse=False):
        # sellconfigs[cls].display()
    cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
    printlog(1, "Get price for city pair %d class %s on %s"
             % (cityPairNo, selling_class, dt1))
    taxes = ReadTaxes(conn, aCompanyCode, dt1, dt2, departAirport,
                      pass_code1='ADULT', pass_code2='CHILD',
                      aState='GP', aNation='ZA',
                      aReturnInd='O')
    rfares = []
    for cls in sorted(sellconfigs, key=sellconfigs.get, reverse=False):
        fare_factor = float(sellconfigs[cls].fare_factor)
        fares = FareCalcDisplay(conn,
                                aCompanyCode,
                                cityPairNo,
                                taxes,
                                dt1,
                                dt2,
                                cls,
                                onw_return_ind,
                                fare_category,
                                authority_level,
                                dt2,
                                fare_factor)
        for fare in fares:
            if fare.selling_class == selling_class:
                fare.apply_taxes(taxes)
                fare.display()
                rfares.append(fare)
    return rfares


def GetPassengers(conn, bn):
    """Read and display passengers in booking."""
    paxRecs = ReadPassengers(conn, bn)
    for paxRec in paxRecs:
        paxRec.display()
    return paxRecs


def GetItinerary(conn, aBookNo):
    """Read and display itenaries for booking."""
    itenRecs = ReadItinerary(conn, aBookNo, '', '')
    for itenRec in itenRecs:
        itenRec.display()
    return itenRecs


def PutBook(conn, vCompany, vBookCategory, vOriginAddress,
            vOriginBranchCode, vAgencyCode,
            groupName, paxRecs,
            aCurrency, payAmount,
            flightNumber, dt1,
            departAirport, arriveAirport,
            sellClass, aFareBasis,
            aTimeLimit,
            vUser, vGroup):
    """Make a booking."""
    if paxRecs is None:
        print("No passenger names")
        return 0, ''
    printlog(1, "Book fare basis %s payment %s%.2f flight %s date %s"
             % (aFareBasis, aCurrency, payAmount, flightNumber, dt1))
    vSeatQuantity = len(paxRecs)
    if payAmount is None:
        payAmount = 0.0
    if sellClass is None:
        sellClass = 'Y'
    #if departAirport is None or arriveAirport is None:
        #print("Flight number and date must be specified")
        #return
    printlog(1, "Book %d seats on flight %s date %s class %s"
             % (vSeatQuantity, flightNumber, dt1, sellClass))
    n, fd = ReadFlightDeparture(conn, sellClass, flightNumber, dt1)
    if n == 0:
        print("Flight number and date not found")
        return 0, ''
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
            dt1, groupName, vUser, vGroup)
    AddItinerary(conn, bn, flightNumber, dt1,
                 departAirport, arriveAirport,
                 departTime, arriveTime,
                 departTerm, arriveTerm,
                 cityPairNo, sellClass,
                 vUser, vGroup)
    AddPassenger(conn, bn, paxRecs, vUser, vGroup)
    AddContact(conn, bn, paxRecs, vUser, vGroup)
    paxRequests = []
    for paxRec in paxRecs:
        paxRequests.append(paxRec.date_of_birth.strftime("%d%b%Y").upper())
    AddBookRequests(conn, bn, vCompany, 'CKIN', paxRequests, vUser, vGroup)
    AddBookTimeLimit(conn, bn, vAgencyCode, vUser, vGroup)
    AddBookingFareSegments(conn, bn, 1, paxRecs[0].passenger_code,
                           departAirport, arriveAirport,
                           flightNumber, dt1,
                           dt1, dt1,
                           sellClass, aFareBasis,
                           aCurrency, payAmount,
                           vUser, vGroup)
    return bn, pnr


def PutPay(conn, aBookNo, aSellClass,
           aCurrency, aPayAmount, aPayAmount2,
           aCompany, aOriginBranchCode, aFareBasisCode,
           vPaymentType, vPaymentForm, vDocNum,
           aUser, aGroup):
    """Process payment."""
    if aBookNo is None:
        print("Book number not specified")
        return 1
    printlog(1, "Process payment of %s%.2f for book %d"
             % (aCurrency, aPayAmount, aBookNo))
    paxRecs = GetPassengers(conn, aBookNo)
    # itenRecs = GetItinerary(conn, aBookNo)
    vPaymentMode = ' '
    vRemark = ' '
    vFareNo = 1
    AddPayment(conn, vPaymentForm, vPaymentType, aCurrency, int(aPayAmount),
               vDocNum, vPaymentMode,
               aBookNo, paxRecs[0].passenger_name, paxRecs[0].passenger_code,
               aOriginBranchCode, vRemark,
               aUser, aGroup)
    # payAmounts = [int(aPayAmount*100), int(aPayAmount2*100)]
    payAmounts = [aPayAmount, aPayAmount2]
    irecs = ReadItinerary(conn, aBookNo, None, None,
                          fnumber=None, start_date=None, end_date=None)
    if len(irecs) > 2:
        print("Found %d itenaries")
        return 1
    else:
        n = 0
        totalPayment = 0
        for irec in irecs:
            irec.display()
            AddBookFares(conn, aBookNo, vFareNo, paxRecs[0].passenger_code,
                         irec.departure_airport, irec.arrival_airport,
                         aCurrency, payAmounts[n], aUser, aGroup)
            AddBookFaresPayments(conn, aBookNo, vFareNo,
                                 paxRecs[0].passenger_code, aFareBasisCode,
                                 aCurrency, payAmounts[n],
                                 aUser, aGroup)
            totalPayment += payAmounts[n]
            n += 1
        AddBookFarePassengers(conn, aBookNo, paxRecs[0].passenger_code,
                              aCurrency, totalPayment,
                              aUser, aGroup)
    UpdateBookPayment(conn, aBookNo, aCurrency, totalPayment)
    UpdateItinerary(conn, aBookNo, 'A')
    UpdateBook(conn, aBookNo, 'A')

    return 0


def DoBook(conn, cfg, lnames, groupName, paxNames, paxDobs, flightNumber, dt1,
           departAirport, arriveAirport,
           departTime, arriveTime,
           sellClass,
           vTimeLimit, payAmount):
    """Do the booking thing."""
    paxRecs = []
    if len(paxNames) == 0:
        if lnames == 0:
            lnames = randint(1, 9)
        n = 0
        while n < lnames:
            # Make the last pax in group a child
            if lnames > 3 and n == lnames-1:
                paxRec = PassengerData('CHILD', n+1)
                paxRec.fakeit(cfg.DialCode, paxRecs[n-1].last_name)
            else:
                paxRec = PassengerData('ADULT', n+1)
                paxRec.fakeit(cfg.DialCode)
            paxRec.display()
            paxRecs.append(paxRec)
            n += 1
    else:
        n = 0
        for paxName in paxNames:
            paxRec = PassengerData('ADULT', n+1, paxName, paxDobs[n])
            paxRecs.append(paxRec)
            n += 1
    if payAmount is None:
        payAmount = 0.0
    if lnames >= 5 and groupName == '':
        groupName = (paxRecs[0].first_name[0] + paxRecs[0].last_name).upper()
    bn, pnr = PutBook(conn, cfg.CompanyCode, cfg.BookCategory, cfg.OriginAddress,
                      cfg.OriginBranchCode, cfg.AgencyCode,
                      groupName, paxRecs,
                      cfg.Currency, payAmount,
                      flightNumber, dt1,
                      departAirport, arriveAirport,
                      # departTime, arriveTime,
                      sellClass, cfg.FareBasisCode,
                      vTimeLimit,
                      cfg.User, cfg.Group)
    if bn > 0:
        print("Created booking %d (%s)" % (bn, pnr))
    return bn


def DoPay(conn, cfg, bn, departAirport, arriveAirport, payAmount, payAmount2,
          vDocNum, sellClass):
    """Process payment for booking."""
    if payAmount is None:
        printlog(1, "Get itinerary for booking %d" % bn)
        itens = GetItinerary(conn, bn)
        payAmount = 0
        for iten in itens:
            printlog(1, "Get price for depart %s arrive %s class %s"
                     % (departAirport, arriveAirport, sellClass))
            fares = GetPrice(conn,
                             cfg.CompanyCode,
                             departAirport, arriveAirport,
                             iten.board_dts, iten.board_dts,
                             sellClass,
                             cfg.OnwReturnIndicator,
                             cfg.FareCategory,
                             cfg.AuthorityLevel)
            for fare in fares:
                payAmount += fare.total_amount
        paxRecs = GetPassengers(conn, bn)
        payAmount *= len(paxRecs)
        printlog(1, "Payment amount not specified: calculated as %.2f" % payAmount)
    vPaymentForm = 'VI'
    vPaymentType = 'CC'
    if vDocNum is None:
        fake = Faker()
        vDocNum = fake.credit_card_number()
    print("Pay %s%.2f with card %s" % (cfg.Currency, payAmount, vDocNum))
    PutPay(conn, bn, sellClass,
            cfg.Currency, payAmount, payAmount2,
            cfg.CompanyCode, cfg.OriginBranchCode, cfg.FareBasisCode,
            vPaymentType, vPaymentForm, vDocNum,
            cfg.User, cfg.Group)


def DoRequest(conn, cfg, aBookNo, pn, reqCode, reqText, payAmount, vDocNum):
    """Add SSR to booking."""
    if payAmount is None:
        fcode, fcurr, payAmount = GetPriceSsr(conn, reqCode)
    vPaymentForm = 'VI'
    vPaymentType = 'CC'
    vPaymentMode = ' '
    vRemark = ' '
    vFareNo = 1
    if vDocNum is None:
        fake = Faker()
        vDocNum = fake.credit_card_number()
    paxRecs = ReadPassengers(conn, aBookNo)
    AddBookRequest(conn, aBookNo, pn, cfg.CompanyCode, reqCode, reqText,
                   cfg.User, cfg.Group)
    AddPayment(conn, fcode, vPaymentType, fcurr, int(payAmount),
               vDocNum, vPaymentMode,
               aBookNo, paxRecs[pn-1].passenger_name,
               paxRecs[pn-1].passenger_code,
               cfg.OriginBranchCode, vRemark,
               cfg.User, cfg.Group)
    return


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
    payAmount = None
    payAmount2 = 0
    sellClass = None
    vTimeLimit = datetime.now() + timedelta(days=2)
    vDocNum = None
    paxCount = 0
    groupName = ''
    reqCode = None
    reqText = None

    # Option flags
    doavail = False
    dochk = False
    dodetail = False
    doprice = False
    dobook = False
    dopay = False
    dossr = False

    if len(argv) < 1:
        usage(os.path.basename(sys.argv[0]))

    opts, args = getopt.getopt(argv,
                               "cfhivyVB:C:D:E:F:G:I:K:L:M:N:P:Q:R:S:T:U:X:Y:",
                               ["help",
                                "avail", "book", "detail", "price", "pay",
                                "chk", "ssr",
                                "bn=", "dob=", "card=", "req=",
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
        elif opt == '--ssr':
            dossr = True
        elif opt in ('-B', '--bn'):
            bn = int(arg)
            printlog(2, "Booking number %d" % bn)
        elif opt in ("-C", "--class"):
            sellClass = str(arg).upper()
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
        elif opt == "-K":
            groupName = str(arg)
        elif opt == "-L":
            paxCount = int(arg)
        elif opt in ("-M", "--dob"):
            paxDobs = str(arg).upper().split(',')
        elif opt in ("-N", "--name"):
            paxNames = str(arg).upper().split(',')
        elif opt in ("-P", "--depart"):
            departAirport = str(arg).upper()
            printlog(1, "\t depart %s" % departAirport)
        elif opt in ("-Q", "--arrive"):
            arriveAirport = str(arg).upper()
            printlog(1, "\t arrive %s" % arriveAirport)
        elif opt in ("-R", "--amount"):
            payAmount = float(arg)
        elif opt in ("-S", "--ramount"):
            payAmount2 = float(arg)
        elif opt in ("-T", "--card"):
            vDocNum = str(arg)
        elif opt in ("-U", "--req"):
            vSsr = str(arg).split(':')
            reqCode =  vSsr[0]
            reqText = vSsr[1]
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

    if sellClass is None:
        sellClass = cfg.SellingClass

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
        GetPrice(conn,
                 cfg.CompanyCode,
                 departAirport, arriveAirport,
                 dt1, dt2,
                 sellClass,  # cfg.SellingClass,
                 cfg.OnwReturnIndicator,
                 cfg.FareCategory,
                 cfg.AuthorityLevel)
    elif dobook:
        bn = DoBook(conn, cfg, paxCount, groupName, paxNames, paxDobs,
                    flightNumber, dt1,
                    departAirport, arriveAirport,
                    departTime, arriveTime,
                    sellClass,
                    vTimeLimit, payAmount)
        if dopay:
            DoPay(conn, cfg, bn,departAirport, arriveAirport,
                  payAmount, payAmount2, vDocNum, sellClass)
    elif dopay:
        DoPay(conn, cfg, bn,departAirport, arriveAirport,
              payAmount, payAmount2, vDocNum, sellClass)
    elif dossr:
        DoRequest(conn, cfg, bn, paxCount, reqCode, reqText, None, None)
    elif bn is not None:
        GetPassengers(conn, bn)
        GetItinerary(conn, bn)
        ReadPayments(conn, bn)
    else:
        print("Nothing to do")

    CloseDb(conn)

    return 0


if __name__ == "__main__":
    """Entry point."""
    rv = main(sys.argv[1:])
    sys.exit(rv)
