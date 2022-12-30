#!/usr/bin/python2 -B
"""
 * @file WriteSsm.cpp
 *
 * Write SSM message
"""

import sys
import getopt
import logging

from Ssm.WriteSsmData import WriteSsmData, GetWeekDay, WriteSsmDataError
from ReadDateTime import ReadDate

logger = logging.getLogger("web2py.app.bars")


def usage(pname):
    """Help message."""
    print("Write flight data :")
    print("\t%s --cnl|--eqt|--new|--rpl|--tim" % (pname))
    print("\t\t -F <FLIGHT> -D <DATE> -Q <FREQ>")
    print("\t\t [-E <DATE>] [-A <CODE>] [-I <TIME>] [-J <TIME>] [-K <CITY>]"
          " [-L <CITY>] [-G <FLIGHT>] [-T <TAIL>]")
    print("\t\t <FILE>")
    print("where")
    print("\t-v\t\t Additional output")
    print("\t--cnl\t\t Cancel flight")
    print("\t--eqt\t\t Equipment change")
    print("\t--new\t\t New flight")
    print("\t--rpl\t\t Replace flight")
    print("\t--tim\t\t Time change")
    print("\t--utc\t\t Time zone UTC (default is LT)")
    print("\t-A <CODE>\t Aircraft code, e.g. 738")
    print("\t-F <FLIGHT>\t Flight number, e.g. JE123")
    print("\t-G <FLIGHT>\t Codeshare flight number, e.g SA2164")
    print("\t-D <DATE>\t Start date, e.g. 11/06/2018")
    print("\t-E <DATE>\t End date, e.g. 11/26/2018")
    print("\t-K <FREQ>\t Frequency code, e.g. 34")
    print("\t-P <CITY>\t Departure airport, e.g. JNB")
    print("\t-Q <CITY>\t Arrival airport, e.g. GRJ")
    print("\t-T <TAIL>\t Tail number")
    print("\t-X <TIME>\t Departure time, e.g. 1120")
    print("\t-Y <TIME>\t Arrival time, e.g. 1325")
    print("\t<FILE>\t\t Output file name (specify '-' for standard output)")
    sys.exit(1)


def main(argv):
    """Pythonic entry point."""
    if len(argv) < 1:
        usage(sys.argv[0])

    ftype = None
    ofname = None
    Address = None
    Sender = None
    SsmTimeZone = 200
    DepartCity = None
    DepartTime = 0
    ArriveCity = None
    ArriveTime = 0
    FlightDateStart = None
    FlightDateEnd = None
    Codeshare = None
    TailNumber = None
    AircraftCode = None
    TimeMode = 'LT'
    FrequencyCode = 0

    try:
        opts, args = getopt.getopt(argv,
                                   "cfhivyV"
                                   "A:B:C:D:E:F:I:K:L:M:N:P:Q:R:S:T:X:Y:",
                                   ["help",
                                    "cnl", "new", "eqt", "rpl",
                                    "date=", "edate=", "flight=",
                                    "period=", "seats=", "days=", "class=",
                                    "locator=", "bookno=",
                                    "depart=", "arrive=",
                                    "aircraft=", "freq=", "cfgtable=",
                                    'msg', 'ssm', 'tim', 'error', 'success',
                                    'cfg', 'contact', 'ssmdata',
                                    'ssmbook'])
    except getopt.GetoptError:
        print("Error in options")
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            usage()
        # elif opt == "--v":
            # show_version(arg)
        elif opt == '-v':
            logger.setLevel(logging.INFO)
        elif opt == '-V':
            logger.setLevel(logging.DEBUG)
        elif opt == "--cnl":
            ftype = "CNL"
        elif opt == "--csv":
            ifname = "-"
        elif opt == "--eqt":
            ftype = "EQT"
        elif opt == "--new":
            ftype = "NEW"
        elif opt == "--rpl":
            ftype = "RPL"
        elif opt == "--tim":
            ftype = "TIM"
        elif opt == "--utc":
            TimeMode = "UTC"
        elif opt == "-A":
            AircraftCode = str(arg)
        elif opt == "-D":
            FlightDateStart = ReadDate(arg)
        elif opt == "-E":
            FlightDateEnd = ReadDate(arg)
        elif opt == "-F":
            FlightNumber = str(arg)
        elif opt == "-G":
            Codeshare = str(arg)
        elif opt == "-I":
            ifname = str(argv)
        elif opt == "-K":
            FrequencyCode = int(arg)
        elif opt == "-P":
            DepartCity = arg
        elif opt == "-Q":
            ArriveCity = arg
        elif opt == "-T":
            TailNumber = arg
        elif opt == "-X":
            if len(arg) == 5 and arg[2] == ':':
                DepartTime = int(arg[3:])
                DepartTime += int(arg[0:2])*100
            else:
                DepartTime = int(arg)
        elif opt == "-Y":
            if len(arg) == 5 and arg[2] == ':':
                ArriveTime = int(arg[3:])
                ArriveTime += int(arg[0:2])*100
            else:
                ArriveTime = int(arg)
        else:
            ofname = arg

    if ftype is None:
        print("File type not specified\n")
        return -1

    if ofname is None:
        ofname = "-"

    if 0 == ArriveTime:
        ArriveTime = DepartTime + 200

    if TimeMode == "UTC":
        DepartTime -= SsmTimeZone
        if DepartTime < 0:
            DepartTime += 2400
            print("Departure time %04d is too complicated"
                  % DepartTime)
            return -1
        ArriveTime -= SsmTimeZone
        if ArriveTime < 0:
            ArriveTime += 2400
            print("Arrival time %04d is too complicated"
                  % ArriveTime)
            return -1

    if len(FlightNumber) and FlightDateStart is not None:
        if FlightDateEnd is None:
            FlightDateEnd = FlightDateStart
        if FrequencyCode == 0:
            FrequencyCode1 = GetWeekDay(FlightDateStart)
            if FlightDateStart != FlightDateEnd:
                FrequencyCode2 = GetWeekDay(FlightDateEnd)
                if FrequencyCode1 <= FrequencyCode2:
                    FrequencyCode = 10*FrequencyCode1+FrequencyCode2
                else:
                    FrequencyCode = 10*FrequencyCode2+FrequencyCode1
            else:
                FrequencyCode = FrequencyCode1
        if ftype == "NEW" or ftype == "TIM":
            if DepartCity is None:
                print("Departure not specified for %s" % ftype)
                return -1
            if ArriveCity is None:
                print("Arrival not specified for %s" % ftype)
                return -1
            if 0 == DepartTime and 0 == ArriveTime:
                print("Departure and/or arrival time not specified for %s"
                      % ftype)
                return -1
            if AircraftCode is None:
                print("Aircraft code not specified for %s" % ftype)
                return -1
        elif ftype == "EQT":
            if AircraftCode is None:
                print("Aircraft code not specified for %s" % ftype)
                return -1
        else:
            # All is well?
            pass

        try:
            ssmData = WriteSsmData(ftype, Address, Sender, TimeMode,
                                   FlightNumber,
                                   FlightDateStart, FlightDateEnd,
                                   DepartCity, DepartTime,
                                   ArriveCity, ArriveTime,
                                   AircraftCode, FrequencyCode,
                                   Codeshare, TailNumber)
            ssmData.WriteSsmFile(ofname)
        except WriteSsmDataError:
            print("SSM processing error\n")
            rc = -1
        except Exception as e:
            print("Processing error: %s" % str(e))
            rc = -1
    else:
        print("Flight number, date and frequency must be specified\n")

    return 0


# Entry point
if __name__ == "__main__":
    rv = main(sys.argv[1:])
    sys.exit(rv)
