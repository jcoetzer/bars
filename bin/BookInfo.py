#!/usr/bin/python3 -B
#
# Python won't try to write .pyc or .pyo files on the import of source modules
#
# @file BookInfo.py
#
"""
Read booking information.
"""

import os
import sys
import getopt
from datetime import datetime, timedelta, date

from BarsLog import set_verbose, printlog
from ReadDateTime import ReadDate
from BarsBanner import print_banner
from Booking.ReadBookingRef import ReadLocator, ReadBookNo
from Booking.ReadBooking import ReadBooking, ReadBookingData
from Booking.ReadBookSummary import ReadBookSummary, ReadBookSummaryHistory
from Booking.BookingPayment import BookingIsPaid
from Booking.ReadRequests import ReadRequestsPnl
from Booking.GraphBookings import GraphBookings
from Flight.ReadFlights import ReadDeparture
from Booking.ReadCrossRef import check_bci, check_bci_trl, check_bci_new
from Booking.BookingSummaryXml import ReadBsItinerary, ReadBsFaresPayment, \
    ReadBsPassengerFares, ReadBsOldFares, \
    ReadBsOldPassengerFares, ReadBsOldFaresPayment, \
    ReadBsFares, ReadBsSummary, \
    ReadBsRetailer
from Booking.ReadItenary import ReadItenary
from DbConnect import OpenDb, CloseDb
from BarsConfig import BarsConfig


# Help message
def usage(pname="BookInfo.py"):

    print_banner()
    # print("Booking information:")
    # print("\t%s [-v|-V] [-n|-t] -A <ORIGIN> -X <EXTLOC> -L <LOCATOR>"
    #       % pname)
    print("Booking payment check:")
    print("\t%s [-v|-V] -p -B <BOOKNO>" % pname)
    print("Booking reminders :")
    print("\t%s [-v|-V] -r -B <BOOKNO>" % pname)
    print("Booking requests:")
    print("\t%s [-v|-V] --ssr -B <BOOKNO> -D <DATE>" % pname)
    print("Check booking cross index:")
    print("\t%s [-v|-V] -t -B <BOOKNO> -X <EXTLOC>" % pname)
    print("\t%s [-v|-V] -t -A <ORIGIN> -B <BOOKNO> -X <EXTLOC>" % pname)
    print("Booking payment data :")
    print("\t%s [-v|-V] --pay -B <BOOKNO>" % pname)
    print("\t%s [-v|-V] --pay -L <LOCATOR>" % pname)
    print("Booking TTY data :")
    print("\t%s [-v|-V] --tty -B <BOOKNO>" % pname)
    print("\t%s [-v|-V] --tty -L <LOCATOR>" % pname)
    print("Booking seating data :")
    print("\t%s [-v|-V] --seat -B <BOOKNO>" % pname)
    print("\t%s [-v|-V] --seat -L <LOCATOR>" % pname)
    print("Booking itenary data :")
    print("\t%s [-v|-V] --itenary -B <BOOKNO>" % pname)
    print("\t%s [-v|-V] --itenary -L <LOCATOR>" % pname)
    print("Booking data :")
    print("\t%s [-v|-V] --book -B <BOOKNO>" % pname)
    print("\t%s [-v|-V] --book -L <LOCATOR>" % pname)
    #print("Booking summary XML data :")
    #print("\t%s [-v|-V] --bs -B <BOOKNO> [-G <AGENCY>] [-K <PAY>]" % pname)
    #print("\t%s [-v|-V] -T <TID>" % pname)
    print("where")
    print("\t-A <ORIGIN>\t Origin address")
    print("\t-B <BOOKNO>\t Booking number")
    print("\t-K <PAY>\t Payment form e.g. 'VI'")
    print("\t-G <AGENCY>\t Agency code")
    print("\t-L <LOCATOR>\t Locator")
    #print("\t-T <TID>\t Transaction ID")
    print("\t-X <EXTLOC>\t External locator")
    # print("\t-U <CURR>\t Currency code : e.g. ZAR")
    sys.exit(1)


def main(argv):
    """Pythonic entry point."""

    status_flag = None
    bookno = None
    dt1 = None
    dt2 = None
    flight_pattrn = None
    flight_number = None
    PassengerName = None
    agency_code = None
    dest_id = None
    action_codes_arg = None
    locator = None
    recCount = None
    ext_book_numb = None
    bci_new = False
    bci_trl = False
    chk_paid = False
    bci_msk = 0
    origin_address = None
    summ_code = None
    hist_code = None
    chk_rem = False
    doGraph = False
    doSsr = False
    doPay = False
    doSeat = False
    doItenary = False
    showTty = False
    doBook = False
    doBsXml = False
    doFaresPayment = False
    payment_form = None

    if len(argv) < 1:
        usage()

    try:
        opts, args = getopt.getopt(argv,
                                   "1234ghlnprtvV"
                                   "A:B:C:D:E:F:G:I:J:K:L:N:P:T:U:X:",
                                   ["help", "ssr", "tty"
                                    "book", "pay", "seat", "itenary", "bs",
                                    "origin=", "bookno=", "end=",
                                    "start=", "create=", "action=", "flight=",
                                    "ext=", "pax=", "pay=",
                                    "dest=", "field=", "locator=", "count=",
                                    "depart=", "delim=", "agency"])
    except getopt.GetoptError:
        print("Error in options")
        # usage()
        sys.exit(1)

    barsdir = os.environ['BARSDIR']
    etcdir = "%s/etc" % barsdir
    lstfiles = {}
    lstfiles['pay'] = ['%s/pay.book_no.lst' % etcdir,
                       '%s/pay.locator.lst' % etcdir]
    lstfiles['tty'] = ['%s/tty.book_no.lst' % etcdir,
                       '%s/tty.locator.lst' % etcdir]
    lstfiles['book'] = ['%s/book.book_no.lst' % etcdir,
                        '%s/book.locator.lst' % etcdir]
    lstfiles['seat'] = ['%s/seat.book_no.lst' % etcdir,
                        '%s/seat.locator.lst' % etcdir]
    lstfiles['itenary'] = ['%s/itenary.book_no.lst' % etcdir]

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            usage()
        elif opt in ("-g", "--graph"):
            doGraph = True
        elif opt == "-l":
            doGraph = True
            try:
                recCount = int(os.environ['LINES'] or 30)
                if recCount > 11:
                    recCount -= 11
            except KeyError:
                recCount = 30
        elif opt == '-n':
            bci_new = True
        elif opt == '-p':
            chk_paid = True
        elif opt == '-r':
            chk_rem = True
        elif opt == "--book":
            doBook = True
        elif opt == "--bs":
            doBsXml = True
        elif opt == "--itenary":
            doItenary = True
        elif opt == "--pay":
            doPay = True
        elif opt == "--seat":
            doSeat = True
        elif opt == "--ssr":
            doSsr = True
            printlog(2, "Check SSR")
        elif opt == '-t':
            bci_trl = True
        elif opt == '-1':
            bci_msk += 1
        elif opt == '-2':
            bci_msk += 2
        elif opt == '-3':
            bci_msk += 4
        elif opt == '-4':
            bci_msk += 8
        elif opt == '-v':
            # Debug output
            set_verbose(1)
        elif opt == '-V':
            # Debug output
            set_verbose(2)
        elif opt in ("-A", "--origin"):
            origin_address = arg
            printlog(2, "origin %s" % origin_address)
        elif opt in ("-B", "--bookno"):
            bookno = int(arg)
            printlog(2, "\t bookno %d" % bookno)
        elif opt in ("-C", "--create"):
            # Create date
            dt1 = ReadDate(arg)
            printlog(2, "\t start %s" % dt1.strftime("%Y-%m-%d"))
        elif opt in ("-D", "--start", "--depart"):
            # Depart date
            dt1 = ReadDate(arg)
            printlog(2, "\t start %s" % dt1.strftime("%Y-%m-%d"))
        elif opt in ("-E", "--end"):
            dt2 = ReadDate(arg)
            printlog(2, "end %s" % dt2.strftime("%Y-%m-%d"))
        elif opt in ("-F", "--flight"):
            if '%' in arg or '_' in arg or len(arg) == 0:
                flight_pattrn = arg
                printlog(2, "\t flight wildcard %s" % flight_number)
            else:
                flight_number = arg
                printlog(2, "flight number %s" % flight_number)
        elif opt in ("-G", "--agency"):
            agency_code = arg
            printlog(2, "agency %s" % agency_code)
        elif opt in ("-I", "--dest"):
            dest_id = str(arg)
            printlog(2, "dest id %s" % dest_id)
        elif opt in ("-K", "--pay"):
            payment_form = arg
        elif opt in ("-L", "--locator"):
            locator = arg
            printlog(2, "locator %s" % locator)
        elif opt in ("-N", "--count"):
            recCount = int(arg)
            printlog(2, "count %d" % recCount)
        elif opt in ("-P", "--pax"):
            PassengerName = arg
        elif opt in ("-X", "--ext"):
            ext_book_numb = str(arg)
        elif opt == "--tty":
            showTty = True
        else:
            print("Unknown option %s" % opt)

    cfg = BarsConfig('%s/bars.cfg' % etcdir)

    # Open connection to database
    conn = OpenDb(cfg.dbname, cfg.dbuser, cfg.dbhost)

    if locator is not None:
        printlog(2, "Read locator %s" % locator)
        bookno = ReadLocator(conn, locator)
    elif bookno is not None:
        printlog(2, "Read booking number %d" % bookno)
        locator = ReadBookNo(conn, bookno)

    if bci_msk == 0:
        bci_msk = 0xf

    if doGraph:
        GraphBookings(conn, recCount, dt1, dt2)
    elif doBsXml:
        ReadBsRetailer(conn, bookno, agency_code, payment_form)
        ReadBsItinerary(conn, bookno)
        ReadBsFares(conn, bookno, cfg.Currency)
        ReadBsOldFares(conn, bookno, cfg.Currency)
        ReadBsPassengerFares(conn, bookno, cfg.Currency)
        ReadBsOldPassengerFares(conn, bookno, cfg.Currency)
        ReadBsFaresPayment(conn, bookno, cfg.Currency)
        ReadBsOldFaresPayment(conn, bookno, cfg.Currency)
        ReadBsSummary(conn, bookno, cfg.Currency)
    elif doSsr and bookno is not None:
        if dt1 is None:
            pnr, dt1 = ReadBooking(conn, bookno)
        irecs = ReadItenary(conn, bookno, None, None,
                            fnumber=None, start_date=None, end_date=None)
        for irec in irecs:
            irec.display()
            n, departure_airport, arrival_airport, city_pair = \
                ReadDeparture(conn, irec.flight_number, dt1)
            if n == 0:
                print("Could not find flight %s on %s"
                      % (irec.flight_number, dt1.strftime("%Y-%m-%d")))
                return 1
            ReadRequestsPnl(conn, bookno, cfg.CompanyCode, departure_airport,
                            dt1, PassengerName)
    elif bci_new and origin_address is not None and ext_book_numb is not None \
            and locator is not None:
        check_bci_new(conn, origin_address, ext_book_numb, locator, bci_msk)
    elif bci_trl and origin_address is not None and ext_book_numb is not None \
            and locator is not None:
        check_bci_trl(conn, origin_address, ext_book_numb, locator)
    elif origin_address is not None and ext_book_numb is not None \
            and locator is not None:
        check_bci(conn, origin_address, ext_book_numb, locator, bci_msk)
    elif chk_paid and bookno is not None:
        ReadBooking(conn, bookno)
        rv = BookingIsPaid(conn, bookno)
        if rv:
            print("Booking %d is paid up" % bookno)
        else:
            print("Booking %d is not paid up" % bookno)
    elif chk_rem and bookno is not None:
        ReadBookSummary(conn, bookno, summ_code)
        ReadBookSummaryHistory(conn, bookno, hist_code)
    elif doPay and bookno is not None and locator is not None:
        ReadBookingData(conn, lstfiles['pay'], bookno, locator)
    elif showTty and bookno is not None and locator is not None:
        ReadBookingData(conn, lstfiles['tty'], bookno, locator)
    elif doBook and bookno is not None:
        ReadBookingData(conn, lstfiles['book'], bookno, None)
    elif doSeat and bookno is not None:
        ReadBookingData(conn, lstfiles['seat'], bookno, None)
    elif doItenary and bookno is not None:
        ReadBookingData(conn, lstfiles['itenary'], bookno, None)
    elif bookno is not None and locator is not None:
        ReadBookingData(conn, lstfiles['pay'], bookno, locator)
    else:
        print("Nothing to do!")

    # Commit transaction and close connection
    CloseDb(conn)

    sys.exit(0)


# Entry point
if __name__ == "__main__":
    main(sys.argv[1:])
