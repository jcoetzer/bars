#!/usr/bin/python
#
# @file ProcSsmYacc.py
#

import sys
import ply.lex as lex
import ply.yacc as yacc

from SsmLex import tokens
from SsmYacc import tokens
from SsmData import SsmData, read_ssm_data
from SsmYacc import YaccFile

import psycopg2
from BarsLog import printlog, set_verbose
from ReadDateTime import ReadDate, DateRange
from ProcNew import ProcNew
from ProcCnl import ProcCnl
from SsmDb import CheckCityPair, CheckFlightPeriod

import psycopg2


def ProcData(conn, ssm, userName, groupName):

    rv = 0
    if ssm.action == 'NEW':
        rv = ProcNew(conn, ssm, userName, groupName)
    elif ssm.action == 'CNL':
        rv = ProcCnl(conn, ssm)
    else:
        print "Unsupported action %s" % ssm.action
        return -1

    return rv


def usage():
    print "Help!"
    sys.exit(1)


# Pythonic entry point
def main(argv):

    global verbose
    fname = None
    rv = 0

    dbname = 'barsdb'

    if len(argv) < 1:
        usage()

    for opt in argv:
        if opt == '-h' or opt == '--help':
            usage()
        elif opt == '-v':
            set_verbose(1)
        elif opt == '-V':
            set_verbose(2)
        else:
            fname = str(opt)

    if fname is None or len(fname)==0:
        print "No input file specified"
        return 1

    # Open connection to database
    try:
        conn = psycopg2.connect("dbname='%s' user='postgres' host='localhost'" % dbname)
    except:
        print "Could not connect to database %s" % dbname
        return 1
    printlog(1, "Connected to database %s" % dbname)

    YaccFile(fname)

    ssm = read_ssm_data()
    ssm.display()

    rv = ProcData(conn, ssm, 'OASIS', 'SSM')

    conn.commit()
    conn.close()
    printlog(1, "Disconnected")

    return rv


# Entry point
if __name__ == "__main__":
    rv = main(sys.argv[1:])
    sys.exit(rv)


