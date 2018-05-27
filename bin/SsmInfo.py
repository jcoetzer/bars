#!/usr/bin/python -B
#
# Python won't try to write .pyc or .pyo files on the import of source modules
#
# @file SsmInfo.py
#

import os
import sys
import subprocess
import getopt
import re
import datetime
import psycopg2

from BarsLog import set_verbose, get_verbose, printlog
from ReadDateTime import ReadDate
from FlightData import FlightData
from ReadSchedPeriod import ReadSchedPeriod, ReadConfigNumberOfSeats
from ReadSsmData import ReadSsmFlightData, ReadSsmBookData, ReadSsmTim
from BarsConfig import BarsConfig
from DbConnect import OpenDb, CloseDb

def check_ssm_file(procssm, fname):
    dtm = os.path.getmtime(fname)
    dts = datetime.datetime.fromtimestamp(dtm).strftime('%Y-%m-%d %H:%M:%S')
    printlog(1, "Check %s %s (%f)" % (fname, dts, dtm))
    procf = "%s -c %s" % (procssm, fname)
    printlog(1, "%s" % procf)
    tmp = None
    try:
        pfile = os.popen(procf)
        tmp = pfile.read()
        pfile.close()
    except KeyboardInterrupt:
        try:
            pfile.close()
        except IOError:
            pass
        return -1
    except IOError:
        pass
    printlog(1, "%s" % tmp)
    if "FAIL" in tmp:
        print "[FAIL] %s %s" % (fname, dts)
        if get_verbose() == 0:
            tlines = tmp.split("\n")
            for tline in tlines:
                if "FAIL" in tline:
                    print "%s" % tline
                elif "PASS" in tline:
                    print "%s" % tline
                else:
                    pass
        print
        return 1
    elif "PASS" in tmp:
        tlines = tmp.split("\n")
        for tline in tlines:
            if "PASS" in tline:
                print "%s" % tline
    else:
        print "[ OK ] %s %s" % (fname, dts)
    print
    return 0


def check_ssm_files(ssmdir, procssm):

    printlog(1, "Read directory %s" % ssmdir)
    fnames = []
    nerr = 0
    for f in os.listdir(ssmdir):
        #print "\t%s " % f,
        n = f.find("emailed")
        if n == -1:
            fname = "%s/%s" % (ssmdir, f)
            ssm_file = False
            asm_file = False
            lines = open(fname, "r")
            for line in lines:
                if re.match("^SSM", line):
                    printlog(1, "\t%s SSM" % f)
                    ssm_file = True
                    break
                elif re.match("^ASM", line):
                    printlog(1, "\t%s ASM" % f)
                    sasm_file = True
                    break
                else:
                    pass
            lines.close()
            if ssm_file:
                fnames.append(fname)
            elif asm_file:
                pass
            else:
                printlog(1, "\t %s not SSM" % f)
        else:
            printlog(1, "\t%s ignore" % f)
    fnames.sort()
    for fname in fnames:
        printlog(1, "Read %s" % fname)
        rv = check_ssm_file(procssm, fname)
        if rv > 0:
            nerr += 1
        elif rv < 0:
            print "\nInterrupted"
            return -1
        else:
            pass
    return nerr


def read_ssm_file(procssm, fname):
    t = os.path.getmtime(fname)
    dt = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    printlog(1, "Read %s %s" % (fname, dt))
    procf = "%s -X %s" % (procssm, fname)
    printlog(1, "%s" % procf)
    #proc = subprocess.Popen(procf, stdout=subprocess.PIPE)
    #tmp = proc.stdout.read()
    tmp = os.popen(procf).read()
    ssm_lines = tmp.split('\n')
    tzone = ''
    flight_number = None
    dt1 = None
    dt2 = None
    depart = None
    arrive = None
    tdep = None
    tarr = None
    aircraft_code = None
    cabin_class = '?'
    cabin_seats = 0
    for ssm_line in ssm_lines:
        printlog(2, "%s" % ssm_line)
        ssm_datas = ssm_line.split(':')
        ssmi = ssm_datas[0]
        if ssmi == "Z":
            tzone = ssm_datas[1]
            printlog(1, "Time zone %s" % tzone)
        elif ssmi == "F":
            flight_number = ssm_datas[1]
            printlog(1, "Flight %s" % flight_number)
        elif ssmi == "D":
            date_data = ssm_datas[1].split(" ")
            dt1 = ReadDate(date_data[0])
            dt2 = ReadDate(date_data[1])
            printlog(1, "From %s to %s" % (dt1.strftime("%Y-%m-%d"), dt2.strftime("%Y-%m-%d")))
        elif ssmi == "L":
            legs = ssm_datas[1].split(" ")
            depart = legs[0]
            tdep = int(legs[1])
            arrive = legs[2]
            tarr = int(legs[3])
            if tzone == 'UTC':
                tdep += 200
                tarr += 200
            printlog(1, "Depart %s %04d arrive %s %d" % (depart, tdep, arrive, tarr))
        elif ssmi == "T":
            configs = ssm_datas[1].split(" ")
            aircraft_code = configs[0]
            printlog(1, "Aircraft code %s" % aircraft_code)
        elif ssmi == "C":
            #cabins = ssm_datas[1].split(" ")
            cabins = ssm_datas[1]
            cabin_class = cabins[0]
            cabin_seats = int(cabins[1:])
            printlog(1, "Cabin class %s seats %d" % (cabin_class, cabin_seats))
        elif ssmi == "S10":
            codeshare = ssm_datas[1]
            printlog(1, "Codeshare %s" % codeshare)
        else:
            pass
    #print "%s" % tmp


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def usage(pname='FlightInfo.py'):
    print "Data for a flight as used by SSM processing :"
    print "\t %s --ssmdata -F <FLIGHT> -D <DATE> [-E <DATE>]" % pname
    print "\t %s --ssmbook -F <FLIGHT> -D <DATE> -R <PERD>" % pname
    print "Read success SSM files:"
    print "\t %s --success [-T <DIR>]" % pname
    print "Read error SSM files:"
    print "\t %s --error [-T <DIR>]" % pname
    print "\nParameters:"
    print "\t -P <CITY>\t departure airport"
    print "\t -Q <CITY>\t arrival airport"


def main(argv):
    """Pythonic entry point."""
    barsdir = os.environ['BARSDIR']
    etcdir = "%s/etc" % barsdir
    flight_number = None
    dt1 = None
    dt2 = None
    asm_ssm = False
    ssm_data = False
    ssm_book = False
    ssm_tim = False
    #pdb.set_trace()
    ssmdir = None
    ssmfile = None
    departure_time = "11:00"
    arrival_time = "13:00"
    departure_airport = None
    arrival_airport = None
    aircraft_code = None

    if len(argv) < 1:
        usage()

    try:
        opts, args = getopt.getopt(argv,
                                   "cfhivyVA:B:C:D:E:F:I:K:L:M:N:P:Q:R:S:T:X:Y:",
                                   ["help","date=","edate=","flight=",
                                    "period=","seats=","days=","class=",
                                    "locator=","bookno=","depart=","arrive=",
                                    "aircraft=","freq=","cfgtable=",
                                    'msg','ssm','tim', 'error', 'success', 'cfg','contact','ssmdata',
                                    'ssmbook'])
    except getopt.GetoptError:
        print "Error in options"
        #usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            usage()
        elif opt == '--ssm':
            asm_ssm = True
        elif opt == '--ssmdata':
            ssm_data = True
        elif opt == '--tim':
            ssm_tim = True
        elif opt == '--ssmbook':
            ssm_book = True
        elif opt == '-A':
            aircraft_code =  str(arg)
        elif opt in ("-D", "--date"):
            dt1 = ReadDate(arg)
            printlog(1, "\t flight date %s" % dt1.strftime("%Y-%m-%d"))
        elif opt in ("-E", "--edate"):
            dt2 = ReadDate(arg)
        elif opt in ("-F", "--flight"):
            if '/' in arg:
                fndata = arg.split('/')
                flight_number = fndata[0]
                dt1 = ReadDate(fndata[1])
            else:
                flight_number = arg
            ssm_data = True
        elif opt in ("-P", "--depart"):
            departure_airport = str(arg).upper()
            printlog(1, "\t depart %s" % departure_airport)
        elif opt in ("-Q", "--arrive"):
            arrival_airport = str(arg).upper()
            printlog(1, "\t arrive %s" % arrival_airport)
        elif opt == '-S':
            ssmfile = arg
        elif opt == '-T':
            ssmdir = arg
        elif opt == '-v':
            # Debug output
            set_verbose(1)
        elif opt == '-V':
            # Debug output
            set_verbose(2)
        elif opt == '-X':
            departure_time = str(arg)
        elif opt == '-Y':
            arrival_time = str(arg)
        else:
            print "Unknown option %s" % opt
            return 1

    procssm = "%s/support/bin/procssm" % os.environ['BARSDIR']
      
    cfg = BarsConfig('%s/bars.cfg' % etcdir)

    # Open connection to database
    conn = OpenDb(cfg.dbname, cfg.dbuser, cfg.dbhost)  

    if ssmfile is not None:
        check_ssm_file(procssm, ssmfile)
    elif flight_number is None:
        pass
    else:
        if ssm_tim and dt1 is not None and dt2 is not None:
            flight = FlightData(cfg.SellingClass, flight_number, dt1,
                                departure_time, arrival_time,
                                departure_airport, arrival_airport,
                                0, company_code, aircraft_code)
            n = ReadSsmTim(conn, flight, dt1, dt2, frequency_code)
            if n == 0:
                CheckSsmTim(conn, flight, sdate, edate, frequency_code, aircraft_code)
        elif ssm_data and dt1 is not None:
            flight = FlightData(cfg.SellingClass, flight_number, dt1,
                                departure_time, arrival_time,
                                departure_airport, arrival_airport,
                                0, company_code, aircraft_code)
            ReadSsmFlightData(conn, flight, dt2)
        elif ssm_book and schedule_period_no is not None and dt1 is not None:
            flight = FlightData(cfg.SellingClass, flight_number, dt1,
                                departure_time, arrival_time,
                                departure_airport, arrival_airport,
                                0, company_code, aircraft_code)
            ReadSsmBookData(conn, flight, schedule_period_no)
        elif asm_ssm:
            if aircraft_code is None:
                print "No value for aircraft code"
                conn.close()
                return 1
            if dt1 is None or dt2 is None:
                print "No value for start and/or end dates"
                conn.close()
                return 1
            if frequency_code is None:
                print "No value for frequency code"
                conn.close()
                return 1
            ConfigTableNo, NoOfSeats = ReadConfigNumberOfSeats(conn,
                                                               aircraft_code)
            viaCities = "%3s#%3s" % (departure_airport, arrival_airport)
            ReadSchedPeriod(conn, dt1, dt2, frequency_code,
                            flight_number, frequency_code, viaCities, ConfigTableNo)
            n = GetFlightDataSsm(conn, flight_number, dt1, dt2, frequency_code)
            if n == 0:
                CheckSsmTim(conn, flight, dt1, dt2, frequency_code, aircraft_code)
        else:
            print "Say again?"

    # Commit transaction and close connection
    conn.commit()
    conn.close()

    return 0


# Entry point
if __name__ == "__main__":
    rv = main(sys.argv[1:])
    sys.exit(rv)
