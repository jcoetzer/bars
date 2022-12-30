#!/usr/bin/python2

import os
import sys
import logging
import getopt
from configobj import ConfigObj
from xml.dom import minidom
import psycopg2
from psycopg2 import extras
from datetime import datetime, timedelta, datetime
from ReadDateTime import ReadDate, ReadTime
from Ssm.SsmDb import CheckCityPair, GetCityPair
from ScheduleData import SsmData
from Ssm.ProcNew import ProcNew, AddAircraftConfig, CheckAircraftConfig, \
    AddAircraft
from BarsConfig import BarsConfig
from DbConnect import OpenDb, CloseDb
from Flight.WriteFares import AddCityPair, AddFareSegments, AddFares, \
    DelFareSegments
from Flight.ReadFares import ReadCityPairs, ReadFareSegments, ReadFareCodes
from Ssm.ReadAircraftConfig import ReadEquipmentConfig, WriteEquipmentConfig
from Flight.ReadFlightBookings import ReadFlightBookings, ReadFlightContacts
from Flight.ReadTaxes import ReadTaxes
from BarsBanner import print_banner

logger = logging.getLogger("web2py.app.bars")


def NewCityPair(conn, departAirport, arriveAirport, userName, groupName):
    """Process new flight."""
    city_pair_id = CheckCityPair(conn,
                                 departAirport,
                                 arriveAirport,
                                 1,
                                 userName,
                                 groupName)
    if city_pair_id == 0:
        city_pair_id = AddCityPair(conn, departAirport,
                                   arriveAirport,
                                   userName, groupName)
    return city_pair_id


def NewFlight(conn, aAddress, aSender, aTimeMode,
              aFlightNumber, aFlightDateStart, aFlightDateEnd,
              aDepartCity, aDepartTime, aArriveCity, aArriveTime,
              aFrequencyCode, aCodeshare, aTailNumber,
              aUserName, aGroupName):
    """Create new flight."""
    eqt = ReadEquipmentConfig(conn, aTailNumber)
    if eqt is None:
        print("Aircraft tail number %s not found" % aTailNumber)
        return
    eqt.display()
    ssm = SsmData(aAddress, aSender, aTimeMode,
                  aFlightNumber, aFlightDateStart, aFlightDateEnd,
                  aDepartCity, aDepartTime, aArriveCity, aArriveTime,
                  eqt.aircraft_code, aFrequencyCode, aCodeshare, aTailNumber,
                  eqt.cabin_codes, eqt.seat_capacities)
    if not ssm.check():
        print("Data error")
        return
    ProcNew(conn, ssm, aUserName, aGroupName)


def NewAircraft(conn, companyCode, tailNumber, aircraftCode, configTable,
                cabinCodes, seatCapacities):
    """Add new aircraft."""


def ReadEquipment(conn, tailNumber):
    """Read equipment."""
    ecfg = ReadEquipmentConfig(conn, tailNumber)
    ecfg.display()


def GetTaxes(conn, aCompanyCode, aFlightDate, aReturnDate, aAirport,
              pass_code1='ADULT', pass_code2='CHILD',
              aState='GP', aNation='ZA',
              aReturnInd='O'):
    taxes = ReadTaxes(conn, aCompanyCode, aFlightDate, aReturnDate, aAirport,
                      pass_code1, pass_code2,
                      aState, aNation,
                      aReturnInd)
    for tax in taxes:
        tax.display()


def usage(pname='BarsFlight.py'):
    """Help message."""
    print_banner()
    print("Add city pair:\n\t%s --city -P <CITY> -Q<CITY>" % pname)
    print("Add fare:\n\t%s --fare -P <CITY> -Q<CITY> -R <AMOUNT>"
          "-D <DATE> -E <DATE>" % pname)
    print("Write flight data :")
    print("\t%s --cnl|--eqt|--new|--rpl|--tim" % pname)
    print("\t\t -F <FLIGHT> -D <DATE> -Q <FREQ>")
    print("\t\t [-E <DATE>] [-A <CODE>] [-X <TIME>] [-Y <TIME>] [-P <CITY>]"
          "[-Q <CITY>] [-G <FLIGHT>] [-T <TAIL>]")
    print("Write aircraft data:")
    print("\t%s --new -A <CODE> -N <NAME>" % pname)
    print("\t%s --new -A <CODE> -U <CODE> -T <TAIL> -I <CABIN> -J <SEATS>" % pname)
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
    print("\t-I <CABIN>\t Comma seperated cabin codes, e.g. 'Y,C'")
    print("\t-J <SEATS>\t Seat capacities for cabins, e.g. '186,2'")
    print("\t-K <FREQ>\t Frequency code for weekdays, e.g. 34 (Monday is 1)")
    print("\t-N <NAME>\t Aircraft name, e.g. 'Boeing 737'")
    print("\t-P <CITY>\t Departure airport, e.g. JNB")
    print("\t-Q <CITY>\t Arrival airport, e.g. CPT")
    print("\t-T <TAIL>\t Tail number, e.g. ZSBZZ")
    print("\t-U <CODE>\t Configuration code, e.g. 738A")
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
    doeqt = False
    dopax = False
    dopnl = False
    dotax = False
    docontact = False
    departDate = None
    arriveDate = None
    payAmount = 0
    departAirport = ''
    arriveAirport = ''
    flightNumber = ''
    codeShare = ''
    departTime = None
    arriveTime = None
    frequencyCode = '1234567'
    aircraftCode = ''
    configTable = ''
    tailNumber = ''
    cabinClasses = []
    seatCapacities = []
    aircraftName = None

    if len(argv) < 1:
        usage()

    try:
        opts, args = getopt.getopt(argv,
                                   "cfhivxyVA:D:E:F:G:I:J:K:N:P:Q:R:T:U:X:Y:",
                                   ["help", "city", "fare", "faredel",
                                    "new", "eqt", "cnl", "tim", "rpl",
                                    "utc", "pax", "contact", "tax", "pnl",
                                    "date=", "edate=", "flight=",
                                    "depart=", "arrive=", "name=",
                                    "share=", "cfg=",
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
            logger.setLevel(logging.INFO)
        elif opt == '-V':
            # Debug output
            logger.setLevel(logging.DEBUG)
        elif opt == "--city":
            docity = True
        elif opt == "--fare":
            dofare = True
        elif opt == "--faredel":
            dofaredel = True
        elif opt == "--eqt":
            doeqt = True
        elif opt == "--new":
            donew = True
        elif opt == "--pax":
            dopax = True
        elif opt == "--pnl":
            dopnl = True
        elif opt == "--tax":
            dotax = True
        elif opt == "--contact":
            docontact = True
        elif opt == "-A" or opt == "--aircraft":
            aircraftCode = str(arg).upper()
            logger.debug("aircraft code %s" % aircraftCode)
        elif opt in ("-D", "--date"):
            departDate = ReadDate(arg)
            logger.debug("start date %s" % departDate.strftime("%Y-%m-%d"))
        elif opt in ("-E", "--edate"):
            arriveDate = ReadDate(arg)
            logger.debug("end date %s" % departDate.strftime("%Y-%m-%d"))
        elif opt in ("-F", "--flight"):
            flightNumber = arg
        elif opt in ("-G", "--share"):
            codeShare = arg
        elif opt in ("-I", "--cabin"):
            cabinClasses = str(arg).split(',')
            logger.debug("classes %s" % cabinClasses)
        elif opt in ("-J", "--seat"):
            seatCapacities = str(arg).split(',')
            logger.debug("seats %s" % seatCapacities)
        elif opt in ("-K", "--freq"):
            frequencyCode = str(arg)
        elif opt in ("-N", "--name"):
            aircraftName = str(arg)
        elif opt in ("-P", "--depart"):
            departAirport = str(arg).upper()
            logger.debug("depart %s" % departAirport)
        elif opt in ("-Q", "--arrive"):
            arriveAirport = str(arg).upper()
            logger.debug("arrive %s" % arriveAirport)
        elif opt in ("-R", "--amount"):
            payAmount = int(arg)
            logger.debug("payment %d" % payAmount)
        elif opt in ("-T", "--tail"):
            tailNumber = str(arg)
            logger.debug("tail number %s" % tailNumber)
        elif opt in ("-U", "--cfg"):
            configTable = str(arg)
            logger.debug("configuration %s" % configTable)
        elif opt == "-X":
            departTime = ReadTime(arg)
            logger.debug("depart time %s" % departTime)
        elif opt == "-Y":
            arriveTime = ReadTime(arg)
            logger.debug("arrive time %s" % arriveTime)
        else:
            print("Unknown option '%s'" % opt)
            return 1

    files = []
    for arg in args:
        files.append(arg.strip())

    cfg = BarsConfig('%s/bars.cfg' % etcdir)

    # Open connection to database
    conn = OpenDb(cfg.dbname, cfg.dbuser, cfg.dbhost)

    if donew and flightNumber != '' \
            and departDate is not None \
            and arriveDate is not None \
            and departTime is not None \
            and arriveTime is not None \
            and departAirport != '' \
            and arriveAirport != '' \
            and frequencyCode != '' \
            and tailNumber != '':
        NewFlight(conn, cfg.Address, cfg.Sender, cfg.TimeMode,
                  flightNumber, departDate, arriveDate,
                  departAirport, departTime, arriveAirport, arriveTime,
                  frequencyCode, codeShare, tailNumber,
                  cfg.User, cfg.Group)
    elif donew and len(cabinClasses) > 0 \
            and len(seatCapacities) > 0 \
            and aircraftCode != '' \
            and tailNumber != '' \
            and configTable != '':
        cfgt = CheckAircraftConfig(conn, cfg.CompanyCode, aircraftCode,
                                   cabinClasses, seatCapacities)
        if cfgt is None:
            WriteEquipmentConfig(conn, cfg.CompanyCode, aircraftCode,
                                 tailNumber, configTable, cabinClasses,
                                 seatCapacities, cfg.User, cfg.Group)
            AddAircraftConfig(conn, cfg.CompanyCode, aircraftCode, configTable,
                              cabinClasses, seatCapacities,
                              cfg.User, cfg.Group)
        else:
            print("Found configuration %s" % cfgt)
            eqt = ReadEquipmentConfig(conn, tailNumber)
            if eqt is None:
                WriteEquipmentConfig(conn, cfg.CompanyCode, aircraftCode,
                                     tailNumber, cfgt, cabinClasses,
                                     seatCapacities, cfg.User, cfg.Group)
            else:
                eqt.display()
    elif donew and aircraftCode != '' \
            and aircraftName != '':
        AddAircraft(conn, aircraftCode, aircraftName)
    elif docity and departAirport != '' \
            and arriveAirport != '':
        NewCityPair(conn, departAirport, arriveAirport,
                    cfg.User, cfg.Group)
    elif dopax and flightNumber != '' and departDate is not None:
        ReadFlightBookings(conn, flightNumber, departDate)
    elif dopnl and flightNumber != '' and departDate is not None:
        ReadFlightBookings(conn, flightNumber, departDate, "A")
    elif docontact and flightNumber != '' and departDate is not None:
        ReadFlightContacts(conn, flightNumber, departDate)
    elif docity:
        ReadCityPairs(conn)
    elif dofare and departAirport != '' \
            and arriveAirport != '' and departDate is not None \
            and arriveDate is not None:
        city_pair = GetCityPair(conn, departAirport, arriveAirport)
        if city_pair > 0:
            AddFareSegments(conn, cfg.CompanyCode,
                            departAirport, arriveAirport, city_pair,
                            departDate, arriveDate, payAmount,
                            cfg.User, cfg.Group)
            AddFares(conn, cfg.CompanyCode, departAirport, arriveAirport,
                     cfg.SellingClasses, cfg.User, cfg.Group)
    elif dofaredel and departAirport != '' \
            and arriveAirport != '' \
            and departDate is not None \
            and arriveDate is not None:
        DelFareSegments(conn, cfg.CompanyCode,
                        departAirport, arriveAirport, departDate, arriveDate)
    elif doeqt and tailNumber != '':
        ReadEquipment(conn, tailNumber)
    elif dofare:
        ReadFareCodes(conn)
        ReadFareSegments(conn)
    elif dotax and departAirport != '' and departDate is not None:
        GetTaxes(conn, cfg.CompanyCode, departDate, arriveDate, departAirport)
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
