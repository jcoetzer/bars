#!/usr/bin/python2
#
# @file ProcSsmYacc.py
#
"""
Process SSM input data.
"""

import os
import sys
import logging
import ply.lex as lex
import ply.yacc as yacc

from Ssm.SsmLex import tokens
from Ssm.SsmYacc import tokens
from Ssm.SsmData import SsmData, read_ssm_data
from Ssm.SsmYacc import YaccFile

import psycopg2
from psycopg2 import extras
from ReadDateTime import ReadDate, DateRange
from Ssm.ProcNew import ProcNew
from Ssm.ProcCnl import ProcCnl
from Ssm.SsmDb import CheckCityPair, CheckFlightPeriod

from BarsConfig import BarsConfig
from DbConnect import OpenDb, CloseDb
from BarsBanner import print_banner

logger = logging.getLogger("web2py.app.bars")


def ProcData(conn, ssm, userName, groupName):
    """Process SSM data."""
    rv = 0
    if ssm.action == 'NEW':
        rv = ProcNew(conn, ssm, userName, groupName)
    elif ssm.action == 'CNL':
        rv = ProcCnl(conn, ssm)
    else:
        print("Unsupported action %s" % ssm.action)
        return -1

    return rv


def usage():
    """TODO Help message."""
    print_banner()
    print("Help!")
    sys.exit(1)


def main(argv):
    """Pythonic entry point."""
    barsdir = os.environ['BARSDIR']
    etcdir = "%s/etc" % barsdir
    fname = None
    rv = 0

    if len(argv) < 1:
        usage()

    for opt in argv:
        if opt == '-h' or opt == '--help':
            usage()
        elif opt == '-v':
            logger.setLevel(logging.INFO)
        elif opt == '-V':
            logger.setLevel(logging.DEBUG)
        else:
            fname = str(opt)

    if fname is None or len(fname) == 0:
        print("No input file specified")
        return 1

    cfg = BarsConfig('%s/bars.cfg' % etcdir)

    # Open connection to database
    conn = OpenDb(cfg.dbname, cfg.dbuser, cfg.dbhost)

    YaccFile(fname)

    ssm = read_ssm_data()
    ssm.display()

    rv = ProcData(conn, ssm, 'OASIS', 'SSM')

    conn.commit()
    conn.close()
    logger.info("Disconnected")

    return rv


# Entry point
if __name__ == "__main__":
    rv = main(sys.argv[1:])
    sys.exit(rv)
